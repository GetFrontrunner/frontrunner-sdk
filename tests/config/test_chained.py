from unittest import TestCase

from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig


class TestStaticFrontrunnerConfig(TestCase):

  def test_no_configs(self):
    config = ChainedFrontrunnerConfig([])
    self.assertIsNone(config.injective_exchange_endpoint)

  def test_found_value_eventually(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(),
      StaticFrontrunnerConfig(injective_exchange_endpoint="https://endpoint"),
    ])

    self.assertEqual(config.injective_exchange_endpoint, "https://endpoint")

  def test_could_not_find_value(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(),
    ])

    self.assertIsNone(config.injective_exchange_endpoint)

  def test_found_multiple_values(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(injective_exchange_endpoint="https://endpoint"),
      StaticFrontrunnerConfig(injective_exchange_endpoint="https://wrong"),
    ])

    self.assertEqual(config.injective_exchange_endpoint, "https://endpoint")
