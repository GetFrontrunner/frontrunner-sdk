from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.validation import validate_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class WithdrawFromSubaccountRequest:
  amount: int
  denom: str
  subaccount_index: Optional[int] = None


@dataclass
class WithdrawFromSubaccountResponse:
  transaction: str


class WithdrawFromSubaccountOperation(FrontrunnerOperation[WithdrawFromSubaccountRequest, WithdrawFromSubaccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  def __init__(self, request: WithdrawFromSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> WithdrawFromSubaccountResponse:
    subaccount = Subaccount.from_wallet_and_index(await deps.wallet(), self.request.subaccount_index)
    response = await deps.injective_chain.withdraw_from_subaccount(
      await deps.wallet(), subaccount.subaccount_id, self.request.amount, self.request.denom
    )

    return WithdrawFromSubaccountResponse(transaction=response.txhash)
