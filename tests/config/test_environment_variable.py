from unittest import TestCase

from frontrunner_sdk.config.environment_variable import EnvironmentVariableFrontrunnerConfig # NOQA


class TestEnvironmentVariableFrontrunnerConfig(TestCase):

  def test_defined_value(self):
    config = EnvironmentVariableFrontrunnerConfig({
      "FR_INJECTIVE_EXCHANGE_AUTHORITY": "authority",
    })
    self.assertEqual(config.injective_exchange_authority, "authority")

  def test_undefined_value(self):
    config = EnvironmentVariableFrontrunnerConfig({})
    self.assertIsNone(config.injective_exchange_authority)

  def test_injective_network_invalid_value(self):
    config = EnvironmentVariableFrontrunnerConfig({
      "FR_INJECTIVE_NETWORK": "<wrong>",
    })
    self.assertIsNone(config.injective_exchange_authority)
