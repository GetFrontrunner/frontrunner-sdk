from unittest import TestCase

from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig


class TestStaticFrontrunnerConfig(TestCase):

  def test_no_configs(self):
    config = ChainedFrontrunnerConfig([])
    self.assertIsNone(config.injective_exchange_authority)

  def test_found_value_eventually(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(),
      StaticFrontrunnerConfig(injective_exchange_authority="authority"),
    ])

    self.assertEqual(config.injective_exchange_authority, "authority")

  def test_could_not_find_value(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(),
    ])

    self.assertIsNone(config.injective_exchange_authority)

  def test_found_multiple_values(self):
    config = ChainedFrontrunnerConfig([
      StaticFrontrunnerConfig(injective_exchange_authority="authority"),
      StaticFrontrunnerConfig(injective_exchange_authority="wrong"),
    ])

    self.assertEqual(config.injective_exchange_authority, "authority")
