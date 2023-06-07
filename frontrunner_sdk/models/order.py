from dataclasses import dataclass
from enum import Enum
from typing import AsyncIterator
from typing import Literal
from typing import Sequence
from typing import Type
from typing import TypeVar

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeOrderHistory # NOQA

from frontrunner_sdk.exceptions import FrontrunnerInjectiveException

T = TypeVar("T", bound="OrderHistory")

InjectiveOrderExecutionType = Literal["limit", "market"]
InjectiveOrderState = Literal["booked", "partial_filled", "filled", "canceled"]
InjectiveOrderType = Literal["buy", "sell", "stop_buy", "stop_sell", "take_buy", "take_sell", "buy_po", "sell_po"]


class OrderType(Enum):
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
      return OrderType.BUY_LONG
    elif self.order.direction == "sell" and not self.order.is_reduce_only:
      return OrderType.BUY_SHORT
    elif self.order.direction == "buy" and self.order.is_reduce_only:
      return OrderType.SELL_SHORT
    elif self.order.direction == "sell" and self.order.is_reduce_only:
      return OrderType.SELL_LONG
    else:
      raise FrontrunnerInjectiveException(
        "Unable to compute Frontrunner order type",
        direction=self.order.direction,
        is_reduce_only=self.order.is_reduce_only,
      )

  def __repr__(self):
    # Custom repr is required to pick up added @property
    return f"{self.__class__.__qualname__}(order={self.order},order_type={self.order_type})"

  @classmethod
  def _from_injective_derivative_order_histories(cls: Type[T], orders: Sequence[DerivativeOrderHistory]) -> Sequence[T]:
    return [cls(order) for order in orders]

  @classmethod
  async def _from_async_iterator(cls: Type[T], orders: AsyncIterator[DerivativeOrderHistory]) -> AsyncIterator[T]:
    async for injective_order in orders:
      yield cls(injective_order.order)


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
