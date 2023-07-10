from unittest import TestCase

from frontrunner_sdk.models.currency import Currency
from frontrunner_sdk.models.denom import Denom


class TestCurrency(TestCase):

  def setUp(self) -> None:
    self.denom = Denom(name="FAKE", peggy="peggyFAKE", decimals=2)

  def test_from_quantity(self):
    currency = Currency.from_quantity(200, self.denom)

    self.assertEqual(currency.quantity, 200)
    self.assertEqual(currency.denom, self.denom)

  def test_from_value(self):
    currency = Currency.from_value(200, self.denom)

    self.assertEqual(currency.value, 200)
    self.assertEqual(currency.denom, self.denom)

  def test_value(self):
    currency = Currency.from_quantity(2 * 100, self.denom)

    self.assertEqual(currency.value, 2)
