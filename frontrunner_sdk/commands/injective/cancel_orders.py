from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.cancel_order import CancelOrder


@dataclass
class CancelAllOrdersRequest:
  pass


@dataclass
class CancelAllOrdersResponse:
  orders: Iterable[DerivativeLimitOrder]
  transaction: Optional[str] = None


class CancelAllOrdersOperation(FrontrunnerOperation[CancelAllOrdersRequest, CancelAllOrdersResponse]):

  def __init__(self, request: CancelAllOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CancelAllOrdersResponse:
    wallet = await deps.wallet()

    open_orders = await deps.injective_chain.get_all_open_orders(wallet)

    if not open_orders:
      return CancelAllOrdersResponse(orders=[])

    injective_market_ids = {order.market_id for order in open_orders}

    response = await deps.injective_chain.cancel_all_orders_for_markets(wallet, injective_market_ids)

    return CancelAllOrdersResponse(
      transaction=response.txhash,
      orders=open_orders,
    )


@dataclass
class CancelOrdersRequest:
  orders: Iterable[CancelOrder]


@dataclass
class CancelOrdersResponse:
  transaction: str


class CancelOrdersOperation(FrontrunnerOperation[CancelOrdersRequest, CancelOrdersResponse]):

  def __init__(self, request: CancelOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.orders:
      raise FrontrunnerArgumentException("Orders cannot be empty")

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CancelOrdersResponse:
    wallet = await deps.wallet()

    response = await deps.injective_chain.cancel_orders(wallet, self.request.orders)

    return CancelOrdersResponse(transaction=response.txhash)
