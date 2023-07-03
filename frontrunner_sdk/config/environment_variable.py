from typing import cast
from typing import Mapping
from typing import Optional

from frontrunner_sdk.config.base import Environment
from frontrunner_sdk.config.base import ENVIRONMENTS
from frontrunner_sdk.config.base import FrontrunnerConfig


class EnvironmentVariableFrontrunnerConfig(FrontrunnerConfig):

  def __init__(self, vars: Mapping[str, str]):
    self.vars = vars

  @property
  def environment(self) -> Optional[str]:
    value = self.vars.get("FR_ENVIRONMENT", None)

    if value in ENVIRONMENTS:
      return cast(Environment, value)

    return None

  @property
  def wallet_mnemonic(self) -> Optional[str]:
    return self.vars.get("FR_WALLET_MNEMONIC", None)

  @property
  def wallet_private_key_hex(self) -> Optional[str]:
    return self.vars.get("FR_WALLET_PRIVATE_KEY_HEX", None)

  @property
  def partner_api_base_url(self) -> Optional[str]:
    return self.vars.get("FR_PARTNER_API_BASE_URL", None)

  @property
  def partner_api_authn_token(self) -> Optional[str]:
    return self.vars.get("FR_PARTNER_API_TOKEN", None)

  @property
  def injective_network(self) -> Optional[Environment]:
    value = self.vars.get("FR_INJECTIVE_NETWORK", None)

    if value in ENVIRONMENTS:
      return cast(Environment, value)

    return None

  @property
  def injective_chain_id(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_CHAIN_ID", None)

  @property
  def injective_exchange_authority(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_EXCHANGE_AUTHORITY", None)

  @property
  def injective_explorer_authority(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_EXPLORER_AUTHORITY", None)

  @property
  def injective_grpc_authority(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_GRPC_AUTHORITY", None)

  @property
  def injective_lcd_base_url(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_LCD_BASE_URL", None)

  @property
  def injective_rpc_base_url(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_RPC_BASE_URL", None)

  @property
  def injective_faucet_base_url(self) -> Optional[str]:
    return self.vars.get("FR_INJECTIVE_FAUCET_BASE_URL", None)

  @property
  def injective_insecure(self) -> Optional[bool]:
    return None if self.vars.get("FR_INJECTIVE_INSECURE",
                                 None) is None else self.vars.get("FR_INJECTIVE_INSECURE") == "true"
