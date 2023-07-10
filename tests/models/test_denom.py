from unittest import TestCase

from frontrunner_sdk.models.denom import Denom


class TestDenom(TestCase):

  def setUp(self) -> None:
    self.denom = Denom(name="FAKE", peggy="peggyFAKE", decimals=3)

  def test_quantity_to_value(self):
    self.assertEqual(self.denom.quantity_to_value(7 * 1_000), 7)

  def test_value_to_quantity(self):
    self.assertEqual(self.denom.value_to_quantity(7), 7 * 1_000)
