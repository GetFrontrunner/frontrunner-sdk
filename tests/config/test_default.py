from unittest import TestCase

from frontrunner_sdk.config import DEFAULT


class TestDefaultFrontrunnerConfig(TestCase):

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
    self.assertEqual("https://partner-api-testnet.getfrontrunner.com/api/v1", DEFAULT.partner_api_base_url)
