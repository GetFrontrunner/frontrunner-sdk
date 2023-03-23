from unittest import TestCase

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFrontrunnerIoC(TestCase):

  def setUp(self):
    self.ioc = FrontrunnerIoC()

  def test_config(self):
    self.assertIsInstance(self.ioc.config, FrontrunnerConfig)

  def test_injective_chain(self):
    self.assertIsInstance(self.ioc.injective_chain, InjectiveChain)
