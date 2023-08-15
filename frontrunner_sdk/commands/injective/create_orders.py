from collections import defaultdict
from dataclasses import dataclass
from typing import List

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.order import OrderType


@dataclass
class CreateOrdersRequest:
  orders: List[Order]


@dataclass
class CreateOrdersResponse:
  transaction: str
  orders: List[Order]


class CreateOrdersOperation(FrontrunnerOperation[CreateOrdersRequest, CreateOrdersResponse]):

  def __init__(self, request: CreateOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not len(self.request.orders):
      raise FrontrunnerArgumentException("Orders cannot be empty")

    orders_by_subaccount_and_market: dict = defaultdict(lambda: defaultdict(list))
    for order in self.request.orders:
      if order.quantity <= 0:
        raise FrontrunnerArgumentException("Order quantity must be > 0", order=order)

      if order.price <= 0 or 1 <= order.price:
        raise FrontrunnerArgumentException("Order price must be within between 0 and 1 exclusive", order=order)

      orders_for_subaccount_and_market = orders_by_subaccount_and_market[order.subaccount_index][order.market_id]
      order_types = set([
        OrderType.from_direction_and_side(order.direction, order.side) for order in orders_for_subaccount_and_market
      ])
      if OrderType.BUY_LONG in order_types and OrderType.BUY_SHORT in order_types:
        raise FrontrunnerArgumentException(
          f"Cannot place both short and long orders in market {order.market_id} from a single subaccount"
        )
      orders_by_subaccount_and_market[order.subaccount_index][order.market_id] += [order]

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CreateOrdersResponse:
    response, order_hashes = await deps.injective_chain.create_orders(await deps.wallet(), self.request.orders)

    orders = [order.with_hash(hash) for order, hash in zip(self.request.orders, order_hashes)]

    return CreateOrdersResponse(
      transaction=response.txhash,
      orders=orders,
    )
