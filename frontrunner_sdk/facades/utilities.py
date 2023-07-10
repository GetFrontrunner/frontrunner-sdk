from typing import Union

from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.currency import Currency


class UtilitiesFacade:

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  def currency_from_quantity(self, quantity: Union[int, str], denom_name: str) -> Currency:
    denom = self.deps.denom_factory[denom_name]

    if isinstance(quantity, str):
      quantity = int(quantity, 10)

    return Currency.from_quantity(quantity, denom)

  def currency_from_value(self, value: Union[int, str], denom_name: str) -> Currency:
    denom = self.deps.denom_factory[denom_name]

    if isinstance(value, str):
      value = int(value, 10)

    return Currency.from_value(value, denom)
