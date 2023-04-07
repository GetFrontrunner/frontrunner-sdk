from typing import Iterable
from typing import List

from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletRequest # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletResponse # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse # NOQA
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet
from frontrunner_sdk.sync import SyncMixin


class InjectiveFacadeAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def create_wallet(self) -> CreateWalletResponse:
    request = CreateWalletRequest()
    return await self._run_operation(CreateWalletOperation, self.deps, request)

  async def fund_wallet_from_faucet(self) -> FundWalletFromFaucetResponse:
    request = FundWalletFromFaucetRequest()
    return await self._run_operation(FundWalletFromFaucetOperation, self.deps, request)

  async def create_orders(self, orders: List[Order]) -> CreateOrdersResponse:
    request = CreateOrdersRequest(orders=orders)
    return await self._run_operation(CreateOrdersOperation, self.deps, request)

  async def cancel_all_orders(self) -> CancelAllOrdersResponse:
    request = CancelAllOrdersRequest()
    return await self._run_operation(CancelAllOrdersOperation, self.deps, request)


class InjectiveFacade(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = InjectiveFacadeAsync(deps)

  def create_wallet(self) -> CreateWalletResponse:
    return self._synchronously(self.impl.create_wallet)

  def fund_wallet_from_faucet(self) -> FundWalletFromFaucetResponse:
    return self._synchronously(self.impl.fund_wallet_from_faucet)

  def create_orders(self, orders: Iterable[Order]) -> CreateOrdersResponse:
    return self._synchronously(self.impl.create_orders, orders)

  def cancel_all_orders(self) -> CancelAllOrdersResponse:
    return self._synchronously(self.impl.cancel_all_orders)
