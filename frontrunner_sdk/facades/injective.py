from datetime import datetime
from typing import Iterable
from typing import List
from typing import Literal
from typing import Optional

from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersResponse # NOQA
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
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksOperation # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksRequest # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksResponse # NOQA
from frontrunner_sdk.commands.injective.get_orders import GetOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.get_orders import GetOrdersRequest
from frontrunner_sdk.commands.injective.get_orders import GetOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsRequest # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsResponse # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesOperation # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesRequest
from frontrunner_sdk.commands.injective.get_trades import GetTradesResponse
from frontrunner_sdk.commands.injective.stream_markets import StreamMarketsOperation # NOQA
from frontrunner_sdk.commands.injective.stream_markets import StreamMarketsRequest # NOQA
from frontrunner_sdk.commands.injective.stream_markets import StreamMarketsResponse # NOQA
from frontrunner_sdk.commands.injective.stream_orders import StreamOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.stream_orders import StreamOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.stream_orders import StreamOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.stream_positions import StreamPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.stream_positions import StreamPositionsRequest # NOQA
from frontrunner_sdk.commands.injective.stream_positions import StreamPositionsResponse # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesOperation # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesRequest # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesResponse # NOQA
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin # NOQA
from frontrunner_sdk.helpers.parameters import as_request_args
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.cancel_order import CancelOrder
from frontrunner_sdk.models.order import InjectiveOrderExecutionType
from frontrunner_sdk.models.order import InjectiveOrderState
from frontrunner_sdk.models.order import InjectiveOrderType
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.sync import SyncMixin


class InjectiveFacadeAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def create_wallet(self, fund_and_initialize: bool = True) -> CreateWalletResponse:
    request = CreateWalletRequest(fund_and_initialize=fund_and_initialize)
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

  async def cancel_orders(self, orders: Iterable[CancelOrder]) -> CancelOrdersResponse:
    request = CancelOrdersRequest(orders=orders)
    return await self._run_operation(CancelOrdersOperation, self.deps, request)

  async def get_account_portfolio(self) -> GetAccountPortfolioResponse:
    request = GetAccountPortfolioRequest()
    return await self._run_operation(GetAccountPortfolioOperation, self.deps, request)

  async def get_order_books(self, market_ids: Iterable[str]) -> GetOrderBooksResponse:
    request = GetOrderBooksRequest(market_ids=market_ids)
    return await self._run_operation(GetOrderBooksOperation, self.deps, request)

  async def get_orders(
    self,
    mine: Optional[bool] = None,
    market_ids: Optional[List[str]] = None,
    subaccount_id: Optional[str] = None,
    direction: Optional[Literal["buy", "sell"]] = None,
    is_conditional: Optional[bool] = None,
    order_types: Optional[List[InjectiveOrderType]] = None,
    state: Optional[InjectiveOrderState] = None,
    execution_types: Optional[List[InjectiveOrderExecutionType]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetOrdersResponse:
    kwargs = as_request_args(locals())
    request = GetOrdersRequest(**kwargs)
    return await self._run_operation(GetOrdersOperation, self.deps, request)

  async def get_positions(
    self,
    mine: bool = False,
    market_ids: Optional[Iterable[str]] = None,
    direction: Optional[Literal["buy", "sell"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetPositionsResponse:
    kwargs = as_request_args(locals())
    request = GetPositionsRequest(**kwargs)
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
    kwargs = as_request_args(locals())
    request = GetTradesRequest(**kwargs)
    return await self._run_operation(GetTradesOperation, self.deps, request)

  async def stream_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
  ) -> StreamTradesResponse:
    kwargs = as_request_args(locals())
    request = StreamTradesRequest(**kwargs)
    return await self._run_operation(StreamTradesOperation, self.deps, request)

  async def stream_markets(
    self,
    market_ids: Iterable[str],
  ) -> StreamMarketsResponse:
    kwargs = as_request_args(locals())
    request = StreamMarketsRequest(**kwargs)
    return await self._run_operation(StreamMarketsOperation, self.deps, request)

  async def stream_orders(
    self,
    market_id: str,
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    subaccount_id: Optional[str] = None,
    order_types: Optional[List[str]] = None,
    state: Optional[str] = None,
    execution_types: Optional[str] = None,
  ) -> StreamOrdersResponse:
    kwargs = as_request_args(locals())
    request = StreamOrdersRequest(**kwargs)
    return await self._run_operation(StreamOrdersOperation, self.deps, request)

  async def stream_positions(
    self,
    mine: bool = False,
    market_ids: Optional[List[str]] = None,
    subaccount_ids: Optional[List[str]] = None,
  ) -> StreamPositionsResponse:
    kwargs = as_request_args(locals())
    request = StreamPositionsRequest(**kwargs)
    return await self._run_operation(StreamPositionsOperation, self.deps, request)


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

  def cancel_orders(self, orders: Iterable[CancelOrder]) -> CancelOrdersResponse:
    return self._synchronously(self.impl.cancel_orders, orders)

  def get_account_portfolio(self) -> GetAccountPortfolioResponse:
    return self._synchronously(self.impl.get_account_portfolio)

  def get_order_books(self, market_ids: Iterable[str]) -> GetOrderBooksResponse:
    return self._synchronously(self.impl.get_order_books, market_ids)

  def get_orders(
    self,
    mine: Optional[bool] = None,
    market_ids: Optional[List[str]] = None,
    subaccount_id: Optional[str] = None,
    direction: Optional[Literal["buy", "sell"]] = None,
    is_conditional: Optional[bool] = None,
    order_types: Optional[List[InjectiveOrderType]] = None,
    state: Optional[InjectiveOrderState] = None,
    execution_types: Optional[List[InjectiveOrderExecutionType]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetOrdersResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_orders, **kwargs)

  def get_positions(
    self,
    mine: bool = False,
    market_ids: Optional[Iterable[str]] = None,
    direction: Optional[Literal["buy", "sell"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetPositionsResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_positions, **kwargs)

  def get_trades(
    self,
    market_ids: Iterable[str],
    mine: bool = False,
    direction: Optional[Literal["buy", "sell"]] = None,
    side: Optional[Literal["maker", "taker"]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
  ) -> GetTradesResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_trades, **kwargs)
