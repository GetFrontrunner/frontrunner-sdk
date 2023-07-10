from unittest import TestCase

from frontrunner_sdk.config.static import StaticFrontrunnerConfig
from frontrunner_sdk.facades.utilities import UtilitiesFacade
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestUtilitiesFacade(TestCase):

  def setUp(self):
    config = StaticFrontrunnerConfig(injective_network="testnet")
    self.deps = FrontrunnerIoC(config)
    self.facade = UtilitiesFacade(self.deps)

  def test_currency_from_quantity(self):
    currency = self.facade.currency_from_quantity(700, "USDC")

    self.assertEqual(currency.quantity, 700)
    self.assertEqual(currency.denom.name, "USDC")

  def test_currency_from_value(self):
    currency = self.facade.currency_from_value(700, "USDC")

    self.assertEqual(currency.value, 700)
    self.assertEqual(currency.denom.name, "USDC")
