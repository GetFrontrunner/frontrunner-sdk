from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class FundWalletFromFaucetRequest:
  wallet: Wallet


@dataclass
class FundWalletFromFaucetResponse:
  message: str


class FundWalletFromFaucetOperation(FrontrunnerOperation[FundWalletFromFaucetRequest, FundWalletFromFaucetResponse]):

  def __init__(self, request: FundWalletFromFaucetRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundWalletFromFaucetResponse:
    response = await deps.injective_faucet.fund_wallet(self.request.wallet.injective_address)
    return FundWalletFromFaucetResponse(message=response["message"])
