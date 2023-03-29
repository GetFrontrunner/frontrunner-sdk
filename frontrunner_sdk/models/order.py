from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
  direction: Literal["buy", "sell"]
  side: Literal["for", "against"]
  market_id: str
  quantity: float
  price: float

  @classmethod
  def buy_for(clz, market_id: str, quantity: float, price: float) -> "Order":
    return clz("buy", "for", market_id, quantity, price)

  @classmethod
  def buy_against(clz, market_id: str, quantity: float, price: float) -> "Order":
    return clz("buy", "against", market_id, quantity, price)

  @classmethod
  def sell_for(clz, market_id: str, quantity: float, price: float) -> "Order":
    return clz("buy", "for", market_id, quantity, price)

  @classmethod
  def sell_against(clz, market_id: str, quantity: float, price: float) -> "Order":
    return clz("buy", "against", market_id, quantity, price)

  @property
  def note(self):
    return f"{self.direction} {self.side} {self.market_id} quantity={self.quantity} @ price={self.price}"
