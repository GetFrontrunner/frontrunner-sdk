import os

from unittest import TestCase

from frontrunner_sdk.config import DEFAULT


class TestFrontrunnerConfig(TestCase):

  def tearDown(self) -> None:
    os.environ.pop("FR_ENVIRONMENT", None)
    os.environ.pop("FR_PRESET_NODES", None)

  def test_defaults(self):
    self.assertEqual("testnet", DEFAULT.environment)
    self.assertEqual("testnet", DEFAULT.injective_network)
    self.assertEqual("injective-888", DEFAULT.injective_chain_id)
    self.assertEqual(False, DEFAULT.injective_insecure)
    self.assertEqual(
      "injective-node-testnet.grpc-exchange.getfrontrunner.com:443", DEFAULT.injective_exchange_authority
    )
    self.assertEqual("injective-node-testnet.grpc.getfrontrunner.com:443", DEFAULT.injective_grpc_authority)
    self.assertEqual("https://injective-node-testnet.lcd.getfrontrunner.com", DEFAULT.injective_lcd_base_url)
    self.assertEqual("wss://injective-node-testnet.tm.getfrontrunner.com/websocket", DEFAULT.injective_rpc_base_url)
    self.assertEqual("k8s.testnet.explorer.grpc.injective.network:443", DEFAULT.injective_explorer_authority)
    self.assertEqual("https://partner-api-testnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)

  def test_testnet_k8s(self):
    os.environ["FR_ENVIRONMENT"] = "testnet"
    os.environ["FR_PRESET_NODES"] = "injective-k8s"
    self.assertEqual("testnet", DEFAULT.environment)
    self.assertEqual("testnet", DEFAULT.injective_network)
    self.assertEqual("injective-888", DEFAULT.injective_chain_id)
    self.assertEqual(False, DEFAULT.injective_insecure)
    self.assertEqual("k8s.testnet.exchange.grpc.injective.network:443", DEFAULT.injective_exchange_authority)
    self.assertEqual("k8s.testnet.chain.grpc.injective.network:443", DEFAULT.injective_grpc_authority)
    self.assertEqual("https://k8s.testnet.lcd.injective.network", DEFAULT.injective_lcd_base_url)
    self.assertEqual("wss://k8s.testnet.tm.injective.network/websocket", DEFAULT.injective_rpc_base_url)
    self.assertEqual("k8s.testnet.explorer.grpc.injective.network:443", DEFAULT.injective_explorer_authority)
    self.assertEqual("https://partner-api-testnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)

  def test_default_mainnet(self):
    os.environ["FR_ENVIRONMENT"] = "mainnet"
    self.assertEqual("mainnet", DEFAULT.environment)
    self.assertEqual("mainnet", DEFAULT.injective_network)
    self.assertEqual("injective-1", DEFAULT.injective_chain_id)
    self.assertEqual(False, DEFAULT.injective_insecure)
    self.assertEqual(
      "injective-node-mainnet.grpc-exchange.getfrontrunner.com:443", DEFAULT.injective_exchange_authority
    )
    self.assertEqual("injective-node-mainnet.grpc.getfrontrunner.com:443", DEFAULT.injective_grpc_authority)
    self.assertEqual("https://injective-node-mainnet.lcd.getfrontrunner.com", DEFAULT.injective_lcd_base_url)
    self.assertEqual("wss://injective-node-mainnet.tm.getfrontrunner.com/websocket", DEFAULT.injective_rpc_base_url)
    self.assertEqual("k8s.global.mainnet.explorer.grpc.injective.network:443", DEFAULT.injective_explorer_authority)
    self.assertEqual("https://partner-api-mainnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)

  def test_mainnet_global(self):
    os.environ["FR_ENVIRONMENT"] = "mainnet"
    os.environ["FR_PRESET_NODES"] = "injective-global"
    self.assertEqual("mainnet", DEFAULT.environment)
    self.assertEqual("mainnet", DEFAULT.injective_network)
    self.assertEqual("injective-1", DEFAULT.injective_chain_id)
    self.assertEqual(False, DEFAULT.injective_insecure)
    self.assertEqual("k8s.global.mainnet.exchange.grpc.injective.network:443", DEFAULT.injective_exchange_authority)
    self.assertEqual("k8s.global.mainnet.chain.grpc.injective.network:443", DEFAULT.injective_grpc_authority)
    self.assertEqual("https://k8s.global.mainnet.lcd.injective.network:443", DEFAULT.injective_lcd_base_url)
    self.assertEqual("wss://k8s.global.mainnet.tm.injective.network:443/websocket", DEFAULT.injective_rpc_base_url)
    self.assertEqual("k8s.global.mainnet.explorer.grpc.injective.network:443", DEFAULT.injective_explorer_authority)
    self.assertEqual("https://partner-api-mainnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)

  def test_mainnet_sentry(self):
    os.environ["FR_ENVIRONMENT"] = "mainnet"
    os.environ["FR_PRESET_NODES"] = "injective-sentry"
    self.assertEqual("mainnet", DEFAULT.environment)
    self.assertEqual("mainnet", DEFAULT.injective_network)
    self.assertEqual("injective-1", DEFAULT.injective_chain_id)
    self.assertEqual(True, DEFAULT.injective_insecure)
    self.assertEqual("sentry0.injective.network:9910", DEFAULT.injective_exchange_authority)
    self.assertEqual("sentry0.injective.network:9900", DEFAULT.injective_grpc_authority)
    self.assertEqual("https://lcd.injective.network", DEFAULT.injective_lcd_base_url)
    self.assertEqual("ws://sentry0.injective.network:26657/websocket", DEFAULT.injective_rpc_base_url)
    self.assertEqual("sentry0.injective.network:9911", DEFAULT.injective_explorer_authority)
    self.assertEqual("https://partner-api-mainnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)
