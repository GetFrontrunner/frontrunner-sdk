from typing import Iterable

from frontrunner_sdk.commands.injective.create_orders import CreateOrdersOperation  # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersRequest  # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersResponse  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletRequest  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletResponse  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse  # NOQA
from frontrunner_sdk.commands.injective.load_wallet_from_mnemonic import LoadWalletFromMnemonicOperation  # NOQA
from frontrunner_sdk.commands.injective.load_wallet_from_mnemonic import LoadWalletFromMnemonicRequest  # NOQA
from frontrunner_sdk.commands.injective.load_wallet_from_mnemonic import LoadWalletFromMnemonicResponse  # NOQA
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet
from frontrunner_sdk.sync import SyncMixin


class InjectiveAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def create_wallet(self) -> CreateWalletResponse:
    request = CreateWalletRequest()
    return await self._run_operation(CreateWalletOperation, self.deps, request)

  async def load_wallet_from_mnemonic(self, mnemonic: str) -> LoadWalletFromMnemonicResponse:
    request = LoadWalletFromMnemonicRequest(mnemonic=mnemonic)
    return await self._run_operation(LoadWalletFromMnemonicOperation, self.deps, request)

  async def fund_wallet_from_faucet(self, wallet: Wallet) -> FundWalletFromFaucetResponse:
    request = FundWalletFromFaucetRequest(wallet=wallet)
    return await self._run_operation(FundWalletFromFaucetOperation, self.deps, request)

  async def create_orders(self, wallet: Wallet, orders: Iterable[Order]) -> CreateOrdersResponse:
    request = CreateOrdersRequest(wallet=wallet, orders=orders)
    return await self._run_operation(CreateOrdersOperation, self.deps, request)


class Injective(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = InjectiveAsync(deps)

  def create_wallet(self) -> CreateWalletResponse:
    return self._synchronously(self.impl.create_wallet)

  def load_wallet_from_mnemonic(self, mnemonic: str) -> LoadWalletFromMnemonicResponse:
    return self._synchronously(self.impl.load_wallet_from_mnemonic, mnemonic)

  def fund_wallet_from_faucet(self, wallet: Wallet) -> FundWalletFromFaucetResponse:
    return self._synchronously(self.impl.fund_wallet_from_faucet, wallet)

  def create_orders(self, wallet: Wallet, orders: Iterable[Order]) -> CreateOrdersResponse:
    return self._synchronously(self.impl.create_orders, wallet, orders)
