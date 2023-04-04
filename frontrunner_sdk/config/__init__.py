import os

from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.conditional import ConditionalFrontrunnerConfig
from frontrunner_sdk.config.environment_variable import EnvironmentVariableFrontrunnerConfig # NOQA
from frontrunner_sdk.config.static import StaticFrontrunnerConfig

DEFAULT_FRONTRUNNER_CONFIG: FrontrunnerConfig = ChainedFrontrunnerConfig([
  EnvironmentVariableFrontrunnerConfig(os.environ),

  # testnet
  StaticFrontrunnerConfig(
    injective_network="testnet",
    injective_chain_id="injective-888",
    injective_faucet_base_url="https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI",
  ),

  # frontrunner api
  StaticFrontrunnerConfig(frontrunner_api_base_url="https://partner-api-staging.getfrontrunner.com/api/v1"),

  # injective k8s network
  ConditionalFrontrunnerConfig(
    lambda: os.environ.get("FRONTRUNNER_PRESET_NODES") == "injective",
    StaticFrontrunnerConfig(
      injective_exchange_authority="k8s.testnet.exchange.grpc.injective.network:443",
      injective_explorer_authority="k8s.testnet.explorer.grpc.injective.network:443",
      injective_grpc_authority="k8s.testnet.chain.grpc.injective.network:443",
      injective_lcd_base_url="https://k8s.testnet.lcd.injective.network",
      injective_rpc_base_url="wss://k8s.testnet.tm.injective.network/websocket",
    )
  ),

  # frontrunner network
  StaticFrontrunnerConfig(
    injective_exchange_authority="injective-node-v2-staging.grpc-exchange.getfrontrunner.com:443",
    injective_explorer_authority="injective-node-v2-staging.grpc-explorer.getfrontrunner.com:443",
    injective_grpc_authority="injective-node-v2-staging.grpc.getfrontrunner.com:443",
    injective_lcd_base_url="https://injective-node-v2-staging.lcd.getfrontrunner.com",
    injective_rpc_base_url="wss://injective-node-v2-staging.tm.getfrontrunner.com/websocket",
  ),
])
