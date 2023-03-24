from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging import log_operation


@dataclass
class FundWalletFromFaucetRequest:
  injective_address: str


@dataclass
class FundWalletFromFaucetResponse:
  message: str
  injective_address: str


class FundWalletFromFaucetOperation(FrontrunnerOperation[FundWalletFromFaucetRequest, FundWalletFromFaucetResponse]):

  def __init__(self, request: FundWalletFromFaucetRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundWalletFromFaucetResponse:
    res = await deps.injective_faucet.fund_wallet(self.request.injective_address)

    return FundWalletFromFaucetResponse(
      message=res["message"],
      injective_address=self.request.injective_address,
    )
