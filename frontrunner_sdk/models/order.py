from dataclasses import dataclass
from enum import Enum
from typing import Literal
from typing import Sequence
from typing import Type
from typing import TypeVar

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeOrderHistory # NOQA

T = TypeVar("T", bound="OrderHistory")

InjectiveOrderExecutionType = Literal["limit", "market"]
InjectiveOrderState = Literal["booked", "partial_filled", "filled", "canceled"]
InjectiveOrderType = Literal["buy", "sell", "stop_buy", "stop_sell", "take_buy", "take_sell", "buy_po", "sell_po"]


class FrOrderType(Enum):
  BUY_LONG = 0
  BUY_SHORT = 1
  SELL_LONG = 2
  SELL_SHORT = 3


@dataclass
class OrderHistory:
  order: DerivativeOrderHistory

  @property
  def order_type(self):
    if self.order.direction == "buy" and not self.order.is_reduce_only:
      return FrOrderType.BUY_LONG
    if self.order.direction == "sell" and not self.order.is_reduce_only:
      return FrOrderType.BUY_SHORT
    if self.order.direction == "buy" and self.order.is_reduce_only:
      return FrOrderType.SELL_SHORT
    if self.order.direction == "sell" and self.order.is_reduce_only:
      return FrOrderType.SELL_LONG

  @classmethod
  def _from_injective_derivative_order_histories(cls: Type[T], orders: Sequence[DerivativeOrderHistory]) -> Sequence[T]:
    return [cls(order) for order in orders]


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
