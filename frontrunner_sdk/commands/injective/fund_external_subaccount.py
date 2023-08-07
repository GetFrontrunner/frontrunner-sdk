from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class FundExternalSubaccountRequest:
  amount: int
  denom: str
  source_subaccount_index: int
  destination_subaccount: Subaccount


@dataclass
class FundExternalSubaccountResponse:
  transaction: str


class FundExternalSubaccountOperation(FrontrunnerOperation[FundExternalSubaccountRequest,
                                                           FundExternalSubaccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  def __init__(self, request: FundExternalSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundExternalSubaccountResponse:
    wallet = await deps.wallet()
    source_subaccount = wallet.subaccount(self.request.source_subaccount_index)
    destination_subaccount = self.request.destination_subaccount
    # Use fund_subaccount_from_bank (MsgDeposit) to send from bank balance shared with subaccount 0 because
    # fund_external_subaccount (MsgExternalTransfer) doesn't work from subaccount 0
    if self.request.source_subaccount_index == 0:
      response = await deps.injective_chain.fund_subaccount_from_bank(
        await deps.wallet(), destination_subaccount.subaccount_id, self.request.amount, self.request.denom
      )
    else:
      response = await deps.injective_chain.fund_external_subaccount(
        await deps.wallet(), source_subaccount.subaccount_id, destination_subaccount.subaccount_id, self.request.amount,
        self.request.denom
      )

    return FundExternalSubaccountResponse(transaction=response.txhash)
