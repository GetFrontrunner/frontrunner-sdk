from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class WithdrawFromSubaccountRequest:
  amount: int
  denom: str
  subaccount_index: int


@dataclass
class WithdrawFromSubaccountResponse:
  transaction: str


class WithdrawFromSubaccountOperation(FrontrunnerOperation[WithdrawFromSubaccountRequest,
                                                           WithdrawFromSubaccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    # Subaccount 0 is shared with the bank balance so cannot be withdrawn
    if not self.request.subaccount_index:
      raise FrontrunnerArgumentException(
        "subaccount_index must be present and > 0", subaccount_index=self.request.subaccount_index
      )

  def __init__(self, request: WithdrawFromSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> WithdrawFromSubaccountResponse:
    wallet = await deps.wallet()
    subaccount = wallet.subaccount(self.request.subaccount_index)
    response = await deps.injective_chain.withdraw_from_subaccount(
      await deps.wallet(), subaccount.subaccount_id, self.request.amount, self.request.denom
    )

    return WithdrawFromSubaccountResponse(transaction=response.txhash)
