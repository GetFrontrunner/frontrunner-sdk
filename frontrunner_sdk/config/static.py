from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.base import NetworkEnvironment


@dataclass(frozen=True)
class StaticFrontrunnerConfig(FrontrunnerConfig):
  injective_network: Optional[NetworkEnvironment] = None
  injective_chain_id: Optional[str] = None
  injective_exchange_authority: Optional[str] = None
  injective_explorer_authority: Optional[str] = None
  injective_grpc_authority: Optional[str] = None
  injective_lcd_base_url: Optional[str] = None
  injective_rpc_base_url: Optional[str] = None
  injective_faucet_base_url: Optional[str] = None
