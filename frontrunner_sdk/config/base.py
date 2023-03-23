from typing import Optional


class FrontrunnerConfig:

  @property
  def injective_exchange_endpoint(self) -> Optional[str]:
    return None

  @property
  def injective_grpc_endpoint(self) -> Optional[str]:
    return None

  @property
  def injective_lcd_endpoint(self) -> Optional[str]:
    return None

  @property
  def injective_rpc_endpoint(self) -> Optional[str]:
    return None
