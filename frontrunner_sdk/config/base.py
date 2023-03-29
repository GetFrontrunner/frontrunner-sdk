from typing import Optional


class FrontrunnerConfig:

  @property
  def injective_exchange_base_url(self) -> Optional[str]:
    return None

  @property
  def injective_grpc_base_url(self) -> Optional[str]:
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
