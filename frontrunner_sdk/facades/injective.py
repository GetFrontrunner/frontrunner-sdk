from datetime import datetime
from typing import Iterable
from typing import List
from typing import Literal
from typing import Optional

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
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioOperation # NOQA
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioRequest # NOQA
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioResponse # NOQA
from frontrunner_sdk.commands.injective.get_my_orders import GetMyOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.get_my_orders import GetMyOrdersRequest
from frontrunner_sdk.commands.injective.get_my_orders import GetMyOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksOperation # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksRequest # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksResponse # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsRequest # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsResponse # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesOperation # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesRequest
from frontrunner_sdk.commands.injective.get_trades import GetTradesResponse
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesOperation # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesRequest # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesResponse # NOQA
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
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

  async def get_account_portfolio(self) -> GetAccountPortfolioResponse:
    request = GetAccountPortfolioRequest()
    return await self._run_operation(GetAccountPortfolioOperation, self.deps, request)

  async def get_order_books(self, market_ids: Iterable[str]) -> GetOrderBooksResponse:
    request = GetOrderBooksRequest(market_ids=market_ids)
    return await self._run_operation(GetOrderBooksOperation, self.deps, request)

  async def get_my_orders(self) -> GetMyOrdersResponse:
    request = GetMyOrdersRequest()
    return await self._run_operation(GetMyOrdersOperation, self.deps, request)

  async def get_positions(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetPositionsResponse:
    request = GetPositionsRequest(
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      start_time=start_time,
      end_time=end_time,
    )
    return await self._run_operation(GetPositionsOperation, self.deps, request)

  async def get_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetTradesResponse:
    request = GetTradesRequest(
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      side=side,
      start_time=start_time,
      end_time=end_time,
    )
    return await self._run_operation(GetTradesOperation, self.deps, request)

  async def stream_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> StreamTradesResponse:
    request = StreamTradesRequest(
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      side=side,
      start_time=start_time,
      end_time=end_time,
    )
    return await self._run_operation(StreamTradesOperation, self.deps, request)


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

  def get_account_portfolio(self) -> GetAccountPortfolioResponse:
    return self._synchronously(self.impl.get_account_portfolio)

  def get_order_books(self, market_ids: Iterable[str]) -> GetOrderBooksResponse:
    return self._synchronously(self.impl.get_order_books, market_ids)

  def get_my_orders(self) -> GetMyOrdersResponse:
    return self._synchronously(self.impl.get_my_orders)

  def get_positions(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetPositionsResponse:
    return self._synchronously(
      self.impl.get_positions,
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      start_time=start_time,
      end_time=end_time,
    )

  def get_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetTradesResponse:
    return self._synchronously(
      self.impl.get_trades,
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      side=side,
      start_time=start_time,
      end_time=end_time,
    )

  def stream_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> StreamTradesResponse:
    return self._synchronously(
      self.impl.stream_trades,
      market_ids=market_ids,
      mine=mine,
      direction=direction,
      side=side,
      start_time=start_time,
      end_time=end_time,
    )
