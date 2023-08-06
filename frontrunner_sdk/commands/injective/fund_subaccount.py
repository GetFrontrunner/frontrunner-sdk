from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.validation import validate_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class FundSubaccountRequest:
  amount: int
  denom: str
  source_subaccount_index: Optional[int] = None
  destination_subaccount_index: Optional[int] = None
  destination_subaccount: Optional[Subaccount] = None


@dataclass
class FundSubaccountResponse:
  transaction: str


class FundSubaccountOperation(FrontrunnerOperation[FundSubaccountRequest, FundSubaccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    if self.request.destination_subaccount_index is None and self.request.destination_subaccount is None:
      raise FrontrunnerArgumentException("Must specify either destination_subaccount_index or destination_subaccount")
    validate_mutually_exclusive(
      "destination_subaccount_index", self.request.destination_subaccount_index, "destination_subaccount",
      self.request.destination_subaccount
    )

  def __init__(self, request: FundSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundSubaccountResponse:
    if self.request.destination_subaccount:
      destination_subaccount = self.request.destination_subaccount
    else:
      destination_subaccount = Subaccount.from_wallet_and_index(
        await deps.wallet(),
        self.request.destination_subaccount_index # type: ignore[arg-type]
      )
    # Use fund_subaccount_from_subaccount (MsgSubaccountTransfer) if source subaccount is provided and non-zero.
    # Otherwise, use fund_subaccount_from_bank (MsgDeposit).
    if self.request.source_subaccount_index:
      source_subaccount = Subaccount.from_wallet_and_index(
        await deps.wallet(),
        self.request.source_subaccount_index,
      )
      response = await deps.injective_chain.fund_subaccount_from_subaccount(
        await deps.wallet(), source_subaccount.subaccount_id, destination_subaccount.subaccount_id, self.request.amount,
        self.request.denom
      )
    else:
      response = await deps.injective_chain.fund_subaccount_from_bank(
        await deps.wallet(), destination_subaccount.subaccount_id, self.request.amount, self.request.denom
      )

    return FundSubaccountResponse(transaction=response.txhash)
