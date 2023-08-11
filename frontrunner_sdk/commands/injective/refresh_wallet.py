from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class RefreshWalletRequest:
  pass


@dataclass
class RefreshWalletResponse:
  wallet: Wallet


class RefreshWalletOperation(FrontrunnerOperation[RefreshWalletRequest, RefreshWalletResponse]):

  def __init__(self, request: RefreshWalletRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> RefreshWalletResponse:
    wallet = await deps.wallet()

    await deps.injective_light_client_daemon.initialize_wallet(wallet)

    return RefreshWalletResponse(wallet=wallet)
