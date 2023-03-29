from unittest import TestCase

from frontrunner_sdk.config.static import StaticFrontrunnerConfig


class TestStaticFrontrunnerConfig(TestCase):

  def test_defined_value(self):
    config = StaticFrontrunnerConfig(injective_exchange_base_url="https://endpoint")
    self.assertEqual(config.injective_exchange_base_url, "https://endpoint")

  def test_undefined_value(self):
    config = StaticFrontrunnerConfig()
    self.assertIsNone(config.injective_exchange_base_url)
