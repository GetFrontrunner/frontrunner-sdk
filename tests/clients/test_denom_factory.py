from unittest import TestCase

from pyinjective.constant import devnet_config
from pyinjective.constant import mainnet_config
from pyinjective.constant import testnet_config

from frontrunner_sdk.clients.denom_factory import DenomFactory


class TestDenomFactory(TestCase):

  def test_init_devnet(self):
    denom = DenomFactory("devnet")["USDC"]
    config = devnet_config["USDC"]

    self.assertEqual(denom.peggy, config["peggy_denom"])
    self.assertEqual(denom.decimals, int(config["decimals"]))

  def test_init_testnet(self):
    denom = DenomFactory("testnet")["USDC"]
    config = testnet_config["USDC"]

    self.assertEqual(denom.peggy, config["peggy_denom"])
    self.assertEqual(denom.decimals, int(config["decimals"]))

  def test_init_mainnet(self):
    denom = DenomFactory("mainnet")["USDC"]
    config = mainnet_config["USDC"]

    self.assertEqual(denom.peggy, config["peggy_denom"])
    self.assertEqual(denom.decimals, int(config["decimals"]))
