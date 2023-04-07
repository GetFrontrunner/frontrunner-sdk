from unittest import TestCase

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.clients.injective_light_client_daemon import InjectiveLightClientDaemon # NOQA
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi


class TestFrontrunnerIoC(TestCase):

  def setUp(self):
    self.ioc = FrontrunnerIoC()

  def test_config(self):
    self.assertIsInstance(self.ioc.config, FrontrunnerConfig)

  def test_wallet_not_configured(self):
    with self.assertRaises(FrontrunnerConfigurationException):
      self.ioc.wallet

  def test_openapi_frontrunner_api(self):
    self.assertIsInstance(self.ioc.openapi_frontrunner_api, FrontrunnerApi)

  def test_injective_chain(self):
    self.assertIsInstance(self.ioc.injective_chain, InjectiveChain)

  def test_injective_faucet(self):
    self.assertIsInstance(self.ioc.injective_faucet, InjectiveFaucet)

  def test_injective_light_client_daemon(self):
    self.assertIsInstance(self.ioc.injective_light_client_daemon, InjectiveLightClientDaemon)
