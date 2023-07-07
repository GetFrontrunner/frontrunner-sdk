from functools import cached_property
from typing import Optional
from typing import TypeVar

from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Network

from frontrunner_sdk.clients.denom_factory import DenomFactory
from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.clients.injective_light_client_daemon import InjectiveLightClientDaemon # NOQA
from frontrunner_sdk.clients.openapi_client import openapi_client # NOQA
from frontrunner_sdk.config import DEFAULT
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.models.wallet import Wallet
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi
from frontrunner_sdk.sync import SyncMixin

Result = TypeVar("Result")


class FrontrunnerIoC(SyncMixin):
  _wallet: Optional[Wallet] = None

  def __init__(self, config: FrontrunnerConfig = DEFAULT):
    self.config = config

  @cached_property
  def network(self) -> Network:
    return Network.custom(
      self.config.injective_lcd_base_url,
      self.config.injective_rpc_base_url,
      self.config.injective_grpc_authority,
      self.config.injective_exchange_authority,
      self.config.injective_explorer_authority,
      self.config.injective_chain_id,
      self.config.injective_network,
    )

  async def wallet(self) -> Wallet:
    if self._wallet:
      return self._wallet

    if self.config.wallet_mnemonic:
      await self.use_wallet(Wallet._from_mnemonic(self.config.wallet_mnemonic))

    elif self.config.wallet_private_key_hex:
      await self.use_wallet(Wallet._from_private_key(self.config.wallet_private_key_hex))

    if self._wallet is None:
      raise FrontrunnerConfigurationException("No wallet configured")

    return self._wallet

  async def use_wallet(self, wallet: Wallet):
    await self.injective_light_client_daemon.initialize_wallet(wallet)
    self._wallet = wallet

  @cached_property
  def denom_factory(self) -> DenomFactory:
    return DenomFactory(self.config.injective_network)

  @cached_property
  def openapi_frontrunner_api(self) -> FrontrunnerApi:
    api = openapi_client(FrontrunnerApi)

    config = api.api_client.configuration

    if self.config.partner_api_base_url:
      config.host = self.config.partner_api_base_url

    if self.config.partner_api_authn_token:
      config.api_key = {
        "Authorization": self.config.partner_api_authn_token,
      }

    return api

  @cached_property
  def injective_composer(self) -> Composer:
    return Composer(network=self.network.env)

  @cached_property
  def injective_client(self) -> AsyncClient:
    return AsyncClient(self.network, self.config.injective_insecure)

  @cached_property
  def injective_light_client_daemon(self) -> InjectiveLightClientDaemon:
    return InjectiveLightClientDaemon(self.config.injective_lcd_base_url)

  @cached_property
  def injective_chain(self) -> InjectiveChain:
    return InjectiveChain(self.injective_composer, self.injective_client, self.network)

  @cached_property
  def injective_faucet(self) -> InjectiveFaucet:
    return InjectiveFaucet(self.config.injective_faucet_base_url)
