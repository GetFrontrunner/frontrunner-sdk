from typing import Callable
from typing import Optional

from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.config.base import NetworkEnvironment


class ConditionalFrontrunnerConfig(FrontrunnerConfig):

  def __init__(self, condition: Callable[[], bool], config: FrontrunnerConfig):
    self.condition = condition
    self.config = config

  @property
  def wallet_mnemonic(self) -> Optional[str]:
    return self.config.wallet_mnemonic if self.condition() else None

  @property
  def wallet_private_key_hex(self) -> Optional[str]:
    return self.config.wallet_private_key_hex if self.condition() else None

  @property
  def partner_api_base_url(self) -> Optional[str]:
    return self.config.partner_api_base_url if self.condition() else None

  @property
  def partner_api_authn_token(self) -> Optional[str]:
    return self.config.partner_api_authn_token if self.condition() else None

  @property
  def injective_network(self) -> Optional[NetworkEnvironment]:
    return self.config.injective_network if self.condition() else None

  @property
  def injective_chain_id(self) -> Optional[str]:
    return self.config.injective_chain_id if self.condition() else None

  @property
  def injective_exchange_authority(self) -> Optional[str]:
    return self.config.injective_exchange_authority if self.condition() else None

  @property
  def injective_explorer_authority(self) -> Optional[str]:
    return self.config.injective_explorer_authority if self.condition() else None

  @property
  def injective_grpc_authority(self) -> Optional[str]:
    return self.config.injective_grpc_authority if self.condition() else None

  @property
  def injective_lcd_base_url(self) -> Optional[str]:
    return self.config.injective_lcd_base_url if self.condition() else None

  @property
  def injective_rpc_base_url(self) -> Optional[str]:
    return self.config.injective_rpc_base_url if self.condition() else None

  @property
  def injective_faucet_base_url(self) -> Optional[str]:
    return self.config.injective_faucet_base_url if self.condition() else None

  @property
  def injective_insecure(self) -> Optional[bool]:
    return self.config.injective_insecure if self.condition() else None
