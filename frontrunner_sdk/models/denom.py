from dataclasses import dataclass


@dataclass(frozen=True)
class Denom:
  name: str
  peggy: str
  decimals: int

  def quantity_to_value(self, quantity: int) -> int:
    return quantity / (10**self.decimals)

  def value_to_quantity(self, value: int) -> int:
    return value * (10**self.decimals)
