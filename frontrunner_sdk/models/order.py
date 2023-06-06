from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Sequence

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeOrderHistory

OrderType = Literal["buy", "sell", "stop_buy", "stop_sell", "take_buy", "take_sell", "buy_po", "sell_po"]
OrderState = Literal["booked", "partial_filled", "filled", "canceled"]
OrderExecutionType = Literal["limit", "market"]


class FrOrderType(Enum):
  BUY_LONG = 0
  BUY_SHORT = 1
  SELL_LONG = 2
  SELL_SHORT = 3

@dataclass
class DerivativeOrderHistoryWrapper:
  order: DerivativeOrderHistory
  frOrderType: FrOrderType = field(init=False)

  def __post_init__(self):
    # https://docs.python.org/3.7/library/dataclasses.html#post-init-processing
    self.frOrderType = self._order_to_fr_order_type(self.order)

  @staticmethod
  def _order_to_fr_order_type(order: DerivativeOrderHistory) -> FrOrderType:
    if order.direction == "buy" and not order.is_reduce_only:
      return FrOrderType.BUY_LONG
    if order.direction == "sell" and not order.is_reduce_only:
      return FrOrderType.BUY_SHORT
    if order.direction == "buy" and order.is_reduce_only:
      return FrOrderType.SELL_SHORT
    if order.direction == "sell" and order.is_reduce_only:
      return FrOrderType.SELL_LONG


def wrap_derivative_order_histories(orders: Sequence[DerivativeOrderHistory]) -> Sequence[DerivativeOrderHistoryWrapper]:
  return [DerivativeOrderHistoryWrapper(order) for order in orders]


@dataclass
class Order:
  direction: Literal["buy", "sell"]
  side: Literal["long", "short"]
  market_id: str
  quantity: int
  price: float

  @classmethod
  def buy_long(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("buy", "long", market_id, quantity, price)

  @classmethod
  def buy_short(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("buy", "short", market_id, quantity, price)

  @classmethod
  def sell_long(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("sell", "long", market_id, quantity, price)

  @classmethod
  def sell_short(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("sell", "short", market_id, quantity, price)
