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

DEFAULT: FrontrunnerConfig = ChainedFrontrunnerConfig([
  EnvironmentVariableFrontrunnerConfig(os.environ),

  # mainnet
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FR_ENVIRONMENT") == "mainnet",
    StaticFrontrunnerConfig(
      injective_network=injective_mainnet_global_network.env,
      injective_chain_id=injective_mainnet_global_network.chain_id,
    )
  ),

  # testnet
  StaticFrontrunnerConfig(
    injective_network=injective_testnet_k8s_network.env,
    injective_chain_id=injective_testnet_k8s_network.chain_id,
    injective_faucet_base_url="https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI",
  ),

  # Injective sentry mainnet
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FR_ENVIRONMENT") == "mainnet" and os.environ.get("FR_PRESET_NODES") == "injective-sentry",
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_mainnet_sentry_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_mainnet_sentry_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_mainnet_sentry_network.grpc_endpoint,
      injective_lcd_base_url=injective_mainnet_sentry_network.lcd_endpoint,
      injective_rpc_base_url=injective_mainnet_sentry_network.tm_websocket_endpoint,
    )
  ),

  # Injective global mainnet
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FR_ENVIRONMENT") == "mainnet" and os.environ.get("FR_PRESET_NODES") == "injective-global",
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_mainnet_global_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_mainnet_global_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_mainnet_global_network.grpc_endpoint,
      injective_lcd_base_url=injective_mainnet_global_network.lcd_endpoint,
      injective_rpc_base_url=injective_mainnet_global_network.tm_websocket_endpoint,
    )
  ),

  # default mainnet: Frontrunner mainnet node endpoints & mainnet API
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FR_ENVIRONMENT") == "mainnet",
    StaticFrontrunnerConfig(
      injective_exchange_authority="injective-node-mainnet.grpc-exchange.getfrontrunner.com:443",
      injective_explorer_authority="injective-node-mainnet.grpc-explorer.getfrontrunner.com:443",
      injective_grpc_authority="injective-node-mainnet.grpc.getfrontrunner.com:443",
      injective_lcd_base_url="https://injective-node-mainnet.lcd.getfrontrunner.com",
      injective_rpc_base_url="wss://injective-node-mainnet.tm.getfrontrunner.com/websocket",
      partner_api_base_url="https://partner-api-mainnet.getfrontrunner.com/api/v1",
    )
  ),

  # Injective k8s testnet
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FR_PRESET_NODES") == "injective-k8s",
    StaticFrontrunnerConfig(
      injective_exchange_authority=injective_testnet_k8s_network.grpc_exchange_endpoint,
      injective_explorer_authority=injective_testnet_k8s_network.grpc_explorer_endpoint,
      injective_grpc_authority=injective_testnet_k8s_network.grpc_endpoint,
      injective_lcd_base_url=injective_testnet_k8s_network.lcd_endpoint,
      injective_rpc_base_url=injective_testnet_k8s_network.tm_websocket_endpoint,
    )
  ),

  # default: frontrunner testnet node & testnet API
  StaticFrontrunnerConfig(
    injective_exchange_authority="injective-node-testnet.grpc-exchange.getfrontrunner.com:443",
    injective_explorer_authority="injective-node-testnet.grpc-explorer.getfrontrunner.com:443",
    injective_grpc_authority="injective-node-testnet.grpc.getfrontrunner.com:443",
    injective_lcd_base_url="https://injective-node-testnet.lcd.getfrontrunner.com",
    injective_rpc_base_url="wss://injective-node-testnet.tm.getfrontrunner.com/websocket",
    partner_api_base_url="https://partner-api-testnet.getfrontrunner.com/api/v1",
  ),
])
