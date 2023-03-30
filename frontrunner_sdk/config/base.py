from typing import Literal
from typing import Optional


class FrontrunnerConfig:

  @property
  def injective_network(self) -> Optional[Literal["devnet", "testnet", "mainnet"]]:
    return None

  @property
  def injective_chain_id(self) -> Optional[str]:
    return None

  @property
  def injective_exchange_authority(self) -> Optional[str]:
    return None

  @property
  def injective_explorer_authority(self) -> Optional[str]:
    return None

  @property
  def injective_grpc_authority(self) -> Optional[str]:
    return None

  @property
  def injective_lcd_base_url(self) -> Optional[str]:
    return None

  @property
  def injective_rpc_base_url(self) -> Optional[str]:
    return None

  @property
  def injective_faucet_base_url(self) -> Optional[str]:
    return None
