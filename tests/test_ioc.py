from unittest import TestCase
from unittest.mock import AsyncMock, MagicMock, patch

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.clients.injective_light_client_daemon import InjectiveLightClientDaemon # NOQA
from frontrunner_sdk.config import DEFAULT # NOQA
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi


class TestFrontrunnerIoC(TestCase):

  @staticmethod
  def ioc_for(**kwargs) -> FrontrunnerIoC:
    return FrontrunnerIoC(StaticFrontrunnerConfig(**kwargs))

  def test_config_default(self):
    ioc = FrontrunnerIoC()
    self.assertIsInstance(ioc.config, FrontrunnerConfig)

  def test_wallet_not_configured(self):
    ioc = self.ioc_for()

    with self.assertRaises(FrontrunnerConfigurationException):
      ioc.wallet

  @patch.object(InjectiveLightClientDaemon, "initialize_wallet", new_callable=AsyncMock)
  def test_wallet_configured_with_mnemonic(self, _initialize_wallet):
    wallet = Wallet._new()

    ioc = self.ioc_for(
      wallet_mnemonic=wallet.mnemonic,
      injective_lcd_base_url="https://lcd.injective.example",
    )

    self.assertIsInstance(ioc.wallet, Wallet)

    _initialize_wallet.assert_awaited_once()

  @patch.object(InjectiveLightClientDaemon, "initialize_wallet", new_callable=AsyncMock)
  def test_wallet_configured_with_private_key_hex(self, _initialize_wallet):
    wallet = Wallet._new()

    ioc = self.ioc_for(
      wallet_private_key_hex=wallet.private_key.to_hex(),
      injective_lcd_base_url="https://lcd.injective.example",
    )

    self.assertIsInstance(ioc.wallet, Wallet)

    _initialize_wallet.assert_awaited_once()

  def test_openapi_frontrunner_api(self):
    ioc = self.ioc_for(frontrunner_api_base_url="http://frontrunner.example")

    self.assertIsInstance(ioc.openapi_frontrunner_api, FrontrunnerApi)

  def test_injective_chain(self):
    ioc = self.ioc_for(
      injective_network="testnet",
      injective_chain_id="injective-888",
      injective_exchange_authority="grpc-exchange.injective.example:443",
      injective_explorer_authority="grpc-explorer.injective.example:443",
      injective_grpc_authority="grpc.injective.example:443",
      injective_lcd_base_url="https://lcd.injective.example",
      injective_rpc_base_url="wss://tm.injective.example",
    )

    self.assertIsInstance(ioc.injective_chain, InjectiveChain)

  def test_injective_faucet(self):
    ioc = self.ioc_for(
      injective_faucet_base_url="https://faucet.injective.example",
    )

    self.assertIsInstance(ioc.injective_faucet, InjectiveFaucet)

  def test_injective_light_client_daemon(self):
    ioc = self.ioc_for(
      injective_lcd_base_url="https://lcd.injective.example",
    )

    self.assertIsInstance(ioc.injective_light_client_daemon, InjectiveLightClientDaemon)
