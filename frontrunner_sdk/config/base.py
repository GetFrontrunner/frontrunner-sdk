import typing

from typing import Literal
from typing import Optional

NetworkEnvironment = Literal["testnet", "mainnet"]
NETWORK_ENVIRONMENTS = set(typing.get_args(NetworkEnvironment))


class FrontrunnerConfig:

  @property
  def wallet_mnemonic(self) -> Optional[str]:
    return None

  @property
  def wallet_private_key_hex(self) -> Optional[str]:
    return None

  @property
  def partner_api_base_url(self) -> Optional[str]:
    return None

  @property
  def partner_api_authn_token(self) -> Optional[str]:
    return None

  @property
  def injective_network(self) -> Optional[NetworkEnvironment]:
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

  @property
  def injective_insecure(self) -> Optional[bool]:
    return None
