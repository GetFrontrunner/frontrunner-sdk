from dataclasses import dataclass

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

@dataclass
class LoadWalletFromPrivateKeyRequest:
  private_key: str


@dataclass
class LoadWalletFromPrivateKeyResponse:
  wallet: Wallet


class LoadWalletFromMnemonicOperation(FrontrunnerOperation[LoadWalletFromMnemonicRequest,
                                                           LoadWalletFromMnemonicResponse]):

  def __init__(self, request: LoadWalletFromMnemonicRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> LoadWalletFromMnemonicResponse:
    wallet = Wallet._from_mnemonic(self.request.mnemonic)
    await deps.injective_light_client_daemon.initialize_wallet(wallet)
    return LoadWalletFromMnemonicResponse(wallet=wallet)

class LoadWalletFromPrivateKeyOperation(FrontrunnerOperation[LoadWalletFromPrivateKeyRequest,
                                                           LoadWalletFromPrivateKeyResponse]):

  def __init__(self, request: LoadWalletFromPrivateKeyRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> LoadWalletFromPrivateKeyResponse:
    wallet = Wallet._from_mnemonic(self.request.private_key)
    # await deps.injective_light_client_daemon.initialize_wallet(wallet)
    return LoadWalletFromPrivateKeyResponse(wallet=wallet)
