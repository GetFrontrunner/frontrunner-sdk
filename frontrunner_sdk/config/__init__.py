import os

from pyinjective.constant import Network

from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.conditional import ConditionalFrontrunnerConfig
from frontrunner_sdk.config.environment_variable import EnvironmentVariableFrontrunnerConfig # NOQA
from frontrunner_sdk.config.static import StaticFrontrunnerConfig

injective_testnet_k8s_network = Network.testnet()
injective_mainnet_global_network = Network.mainnet(node="lb")
injective_mainnet_sentry_network = Network.mainnet(node="sentry0")


def fr_injective_network():
  return os.environ.get("FR_INJECTIVE_NETWORK", "testnet")


def should_use_node_set(injective_network: str, endpoint_set_identifier: str):
  return fr_injective_network() == injective_network and \
    os.environ.get("FR_PRESET_NODES", "frontrunner") == endpoint_set_identifier


DEFAULT: FrontrunnerConfig = ChainedFrontrunnerConfig([
  EnvironmentVariableFrontrunnerConfig(os.environ),

  # Injective chain configs #
  ConditionalFrontrunnerConfig(
    lambda: fr_injective_network() == "mainnet",
    StaticFrontrunnerConfig(
      injective_network=injective_mainnet_global_network.env,
      injective_chain_id=injective_mainnet_global_network.chain_id,
      partner_api_base_url="https://partner-api-mainnet.getfrontrunner.com/api/v1",
    )
  ),
  StaticFrontrunnerConfig(
    injective_network=injective_testnet_k8s_network.env,
    injective_chain_id=injective_testnet_k8s_network.chain_id,
    injective_faucet_base_url="https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI",
  ),

  # Injective node endpoints and Frontrunner API endpoint config #
  ConditionalFrontrunnerConfig(
    lambda: should_use_node_set("mainnet", "injective-sentry"),
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_mainnet_sentry_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_mainnet_sentry_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_mainnet_sentry_network.grpc_endpoint,
      injective_lcd_base_url=injective_mainnet_sentry_network.lcd_endpoint,
      injective_rpc_base_url=injective_mainnet_sentry_network.tm_websocket_endpoint,
      injective_insecure=True,
    )
  ),
  ConditionalFrontrunnerConfig(
    lambda: should_use_node_set("mainnet", "injective-global"),
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_mainnet_global_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_mainnet_global_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_mainnet_global_network.grpc_endpoint,
      injective_lcd_base_url=injective_mainnet_global_network.lcd_endpoint,
      injective_rpc_base_url=injective_mainnet_global_network.tm_websocket_endpoint,
    )
  ),

  # default mainnet config
  ConditionalFrontrunnerConfig(
    lambda: should_use_node_set("mainnet", "frontrunner"),
    StaticFrontrunnerConfig(
      injective_exchange_authority="injective-node-mainnet.grpc-exchange.getfrontrunner.com:443",
      # Frontrunner doesn't run the explorer, so use Injective's endpoint regardless
      injective_explorer_authority=injective_mainnet_global_network.grpc_explorer_endpoint,
      injective_grpc_authority="injective-node-mainnet.grpc.getfrontrunner.com:443",
      injective_lcd_base_url="https://injective-node-mainnet.lcd.getfrontrunner.com",
      injective_rpc_base_url="wss://injective-node-mainnet.tm.getfrontrunner.com/websocket",
    )
  ),
  ConditionalFrontrunnerConfig(
    lambda: should_use_node_set("testnet", "injective-k8s"),
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_testnet_k8s_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_testnet_k8s_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_testnet_k8s_network.grpc_endpoint,
      injective_lcd_base_url=injective_testnet_k8s_network.lcd_endpoint,
      injective_rpc_base_url=injective_testnet_k8s_network.tm_websocket_endpoint,
    )
  ),

  # default testnet config
  ConditionalFrontrunnerConfig(
    lambda: should_use_node_set("testnet", "frontrunner"),
    StaticFrontrunnerConfig(
      injective_exchange_authority="injective-node-testnet.grpc-exchange.getfrontrunner.com:443",
      # Frontrunner doesn't run the explorer, so use Injective's endpoint regardless
      injective_explorer_authority=injective_testnet_k8s_network.grpc_explorer_endpoint,
      injective_grpc_authority="injective-node-testnet.grpc.getfrontrunner.com:443",
      injective_lcd_base_url="https://injective-node-testnet.lcd.getfrontrunner.com",
      injective_rpc_base_url="wss://injective-node-testnet.tm.getfrontrunner.com/websocket",
    )
  ),
  StaticFrontrunnerConfig(
    injective_network="testnet",
    partner_api_base_url="https://partner-api-testnet.getfrontrunner.com/api/v1",
    injective_insecure=False,
  )
])
