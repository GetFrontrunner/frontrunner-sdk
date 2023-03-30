from dataclasses import dataclass
from typing import Literal
from typing import Optional

from frontrunner_sdk.config.base import FrontrunnerConfig


@dataclass(frozen=True)
class StaticFrontrunnerConfig(FrontrunnerConfig):
  injective_network: Optional[Literal["devnet", "testnet", "mainnet"]] = None
  injective_chain_id: Optional[str] = None
  injective_exchange_authority: Optional[str] = None
  injective_explorer_authority: Optional[str] = None
  injective_grpc_authority: Optional[str] = None
  injective_lcd_base_url: Optional[str] = None
  injective_rpc_base_url: Optional[str] = None
  injective_faucet_base_url: Optional[str] = None
