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

  @classmethod
  def from_injective_params(cls, direction: str, is_reduce_only: bool):
    if direction == "buy" and not is_reduce_only:
      return cls.BUY_LONG
    elif direction == "sell" and not is_reduce_only:
      return cls.BUY_SHORT
    elif direction == "buy" and is_reduce_only:
      return cls.SELL_SHORT
    elif direction == "sell" and is_reduce_only:
      return cls.SELL_LONG
    else:
      raise FrontrunnerInjectiveException(
        "Unable to compute Frontrunner order type",
        direction=direction,
        is_reduce_only=is_reduce_only,
      )

  @classmethod
  def from_direction_and_side(cls, direction: str, side: str):
    if direction == "buy" and side == "long":
      return cls.BUY_LONG
    elif direction == "buy" and side == "short":
      return cls.BUY_SHORT
    elif direction == "sell" and side == "short":
      return cls.SELL_SHORT
    elif direction == "sell" and side == "long":
      return cls.SELL_LONG
    else:
      raise FrontrunnerInjectiveException(
        "Unable to compute Frontrunner order type",
        direction=direction,
        side=side,
      )


@dataclass
class OrderHistory:
  order: DerivativeOrderHistory

  @property
  def order_type(self):
    return OrderType.from_injective_params(self.order.direction, self.order.is_reduce_only)

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
  subaccount_index: int
  is_post_only: bool

  @classmethod
  def buy_long(clz, market_id: str, quantity: int, price: float, subaccount_index: int = 0, is_post_only: bool = False) -> "Order":
    return clz("buy", "long", market_id, quantity, price, subaccount_index, is_post_only)

  @classmethod
  def buy_short(clz, market_id: str, quantity: int, price: float, subaccount_index: int = 0, is_post_only: bool = False) -> "Order":
    return clz("buy", "short", market_id, quantity, price, subaccount_index, is_post_only)

  @classmethod
  def sell_long(clz, market_id: str, quantity: int, price: float, subaccount_index: int = 0, is_post_only: bool = False) -> "Order":
    return clz("sell", "long", market_id, quantity, price, subaccount_index, is_post_only)

  @classmethod
  def sell_short(clz, market_id: str, quantity: int, price: float, subaccount_index: int = 0, is_post_only: bool = False) -> "Order":
    return clz("sell", "short", market_id, quantity, price, subaccount_index, is_post_only)
