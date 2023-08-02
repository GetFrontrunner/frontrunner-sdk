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
  subaccount_index: Optional[int] = None
  subaccount: Optional[Subaccount] = None


@dataclass
class FundSubaccountResponse:
  transaction: str


class FundSubaccountOperation(FrontrunnerOperation[FundSubaccountRequest, FundSubaccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    if self.request.subaccount_index is None and self.request.subaccount is None:
      raise FrontrunnerArgumentException("Must specify either subaccount_index or subaccount")
    validate_mutually_exclusive(
      "subaccount_index", self.request.subaccount_index, "subaccount", self.request.subaccount
    )

  def __init__(self, request: FundSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundSubaccountResponse:
    subaccount = self.request.subaccount if self.request.subaccount else Subaccount.from_wallet_and_index(
      await deps.wallet(),
      self.request.subaccount_index # type: ignore[arg-type]
    )
    response = await deps.injective_chain.fund_subaccount(
      await deps.wallet(), subaccount.subaccount_id, self.request.amount, self.request.denom
    )

    return FundSubaccountResponse(transaction=response.txhash)
