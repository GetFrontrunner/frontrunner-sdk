from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class FundExternalAccountRequest:
  amount: int
  denom: str
  destination_injective_address: str


@dataclass
class FundExternalAccountResponse:
  transaction: str


class FundExternalAccountOperation(FrontrunnerOperation[FundExternalAccountRequest, FundExternalAccountResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  def __init__(self, request: FundExternalAccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundExternalAccountResponse:
    wallet = await deps.wallet()
    response = await deps.injective_chain.fund_account_from_bank(
      wallet, self.request.destination_injective_address, self.request.amount, self.request.denom
    )
    return FundExternalAccountResponse(transaction=response.txhash)
