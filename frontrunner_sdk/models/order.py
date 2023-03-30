from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
  direction: Literal["buy", "sell"]
  side: Literal["for", "against"]
  market_id: str
  quantity: int
  price: float

  @classmethod
  def buy_for(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("buy", "for", market_id, quantity, price)

  @classmethod
  def buy_against(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("buy", "against", market_id, quantity, price)

  @classmethod
  def sell_for(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("sell", "for", market_id, quantity, price)

  @classmethod
  def sell_against(clz, market_id: str, quantity: int, price: float) -> "Order":
    return clz("sell", "against", market_id, quantity, price)
