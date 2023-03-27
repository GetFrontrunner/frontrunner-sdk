from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.config.base import FrontrunnerConfig


@dataclass(frozen=True)
class StaticFrontrunnerConfig(FrontrunnerConfig):
  injective_exchange_endpoint: Optional[str] = None
  injective_grpc_endpoint: Optional[str] = None
  injective_lcd_endpoint: Optional[str] = None
  injective_rpc_endpoint: Optional[str] = None
  injective_faucet_base_url: Optional[str] = None
