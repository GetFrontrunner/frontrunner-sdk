from unittest import TestCase

from frontrunner_sdk.config.conditional import ConditionalFrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig


class TestConditionalFrontrunnerConfig(TestCase):

  def setUp(self):
    self.base = StaticFrontrunnerConfig(injective_exchange_authority="authority")

  def test_conditional_true(self):
    config = ConditionalFrontrunnerConfig(lambda: True, self.base)
    self.assertEqual(config.injective_exchange_authority, "authority")

  def test_conditional_false(self):
    config = ConditionalFrontrunnerConfig(lambda: False, self.base)
    self.assertIsNone(config.injective_exchange_authority)
