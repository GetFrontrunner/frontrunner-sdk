from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class CreateWalletRequest:
  fund_and_initialize: Optional[bool] = None


@dataclass
class CreateWalletResponse:
  wallet: Wallet


class CreateWalletOperation(FrontrunnerOperation[CreateWalletRequest, CreateWalletResponse]):

  def __init__(self, request: CreateWalletRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CreateWalletResponse:
    wallet = Wallet._new()

    if self.request.fund_and_initialize:
      await deps.injective_faucet.fund_wallet(wallet)
      await deps.use_wallet(wallet)

    return CreateWalletResponse(wallet=wallet)
