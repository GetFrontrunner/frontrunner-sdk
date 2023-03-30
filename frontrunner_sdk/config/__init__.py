from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig

DEFAULT_FRONTRUNNER_CONFIG: FrontrunnerConfig = ChainedFrontrunnerConfig([

  # TODO hardcoding as proof of concept, will have other configs later
  StaticFrontrunnerConfig(
    injective_network="testnet",
    injective_chain_id="injective-888",
    injective_exchange_authority="injective-node-v2-staging.grpc-exchange.getfrontrunner.com",
    injective_explorer_authority="injective-node-v2-staging.grpc-explorer.getfrontrunner.com",
    injective_grpc_authority="injective-node-v2-staging.grpc.getfrontrunner.com",
    injective_lcd_base_url="https://injective-node-v2-staging.lcd.getfrontrunner.com",
    injective_rpc_base_url="wss://injective-node-v2-staging.tm.getfrontrunner.com/websocket",
    injective_faucet_base_url="https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI",
  ),
])
