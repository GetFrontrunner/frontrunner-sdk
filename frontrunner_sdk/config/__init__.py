from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.chained import ChainedFrontrunnerConfig
from frontrunner_sdk.config.static import StaticFrontrunnerConfig

DEFAULT_FRONTRUNNER_CONFIG: FrontrunnerConfig = ChainedFrontrunnerConfig([

  # TODO hardcoding as proof of concept, will have other configs later
  StaticFrontrunnerConfig(
    injective_exchange_endpoint="injective-node-v2-staging.grpc-exchange.getfrontrunner.com",
    injective_grpc_endpoint="injective-node-v2-staging.grpc.getfrontrunner.com",
    injective_lcd_endpoint="injective-node-v2-staging.lcd.getfrontrunner.com",
    injective_rpc_endpoint="injective-node-v2-staging.tm.getfrontrunner.com",
    injective_faucet_base_url="https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI",
  ),
])
