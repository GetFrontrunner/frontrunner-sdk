from dataclasses import dataclass
from typing import Any

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class LoadWalletFromMnemonicRequest:
  mnemonic: str


@dataclass
class LoadWalletFromMnemonicResponse:
  wallet: Wallet


# yapf: disable
class LoadWalletFromMnemonicOperation(
  FrontrunnerOperation[LoadWalletFromMnemonicRequest, LoadWalletFromMnemonicResponse]
):
  # yapf: enable

  def __init__(self, request: LoadWalletFromMnemonicRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> LoadWalletFromMnemonicResponse:
    wallet = Wallet._from_mnemonic(self.request.mnemonic)
    await deps.injective_light_client_daemon.initialize_wallet(wallet)
    return LoadWalletFromMnemonicResponse(wallet=wallet)
