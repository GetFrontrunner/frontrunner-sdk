from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class FundExternalWalletRequest:
  amount: int
  denom: str
  destination_injective_address: str


@dataclass
class FundExternalWalletResponse:
  transaction: str


class FundExternalWalletOperation(FrontrunnerOperation[FundExternalWalletRequest, FundExternalWalletResponse]):

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  def __init__(self, request: FundExternalWalletRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundExternalWalletResponse:
    wallet = await deps.wallet()
    response = await deps.injective_chain.fund_external_wallet_from_bank(
      wallet, self.request.destination_injective_address, self.request.amount, self.request.denom
    )
    return FundExternalWalletResponse(transaction=response.txhash)
