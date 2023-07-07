from dataclasses import dataclass

from frontrunner_sdk.clients.denom_factory import Denom


@dataclass(frozen=True)
class Currency:
  quantity: int
  denom: Denom

  @classmethod
  def from_quantity(clz, quantity: int, denom: Denom) -> "Currency":
    return Currency(quantity=quantity, denom=denom)

  @classmethod
  def from_value(clz, value: int, denom: Denom) -> "Currency":
    return Currency(quantity=denom.value_to_quantity(value), denom=denom)

  @property
  def value(self) -> int:
    return self.denom.quantity_to_value(self.quantity)
