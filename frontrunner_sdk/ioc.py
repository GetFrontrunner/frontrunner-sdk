from functools import cached_property

from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Network

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.clients.injective_light_client_daemon import InjectiveLightClientDaemon # NOQA
from frontrunner_sdk.config import DEFAULT_FRONTRUNNER_CONFIG
from frontrunner_sdk.config import FrontrunnerConfig
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi


class FrontrunnerIoC:

  @property
  def config(self) -> FrontrunnerConfig:
    return DEFAULT_FRONTRUNNER_CONFIG

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

  @cached_property
  def frontrunner_api(self) -> FrontrunnerApi:
    api = FrontrunnerApi()

    config = api.api_client.configuration

    if self.config.frontrunner_api_base_url:
      config.host = self.config.frontrunner_api_base_url

    if self.config.frontrunner_api_authn_token:
      config.api_key = {
        "Authorization": self.config.frontrunner_api_authn_token,
      }

    return api

  @cached_property
  def injective_composer(self) -> Composer:
    return Composer(network=self.network)

  @cached_property
  def injective_client(self) -> AsyncClient:
    return AsyncClient(self.network)

  @cached_property
  def injective_light_client_daemon(self) -> InjectiveLightClientDaemon:
    return InjectiveLightClientDaemon(self.config.injective_lcd_base_url)

  @cached_property
  def injective_chain(self) -> InjectiveChain:
    return InjectiveChain(self.injective_composer, self.injective_client, self.network)

  @cached_property
  def injective_faucet(self) -> InjectiveFaucet:
    return InjectiveFaucet(self.config.injective_faucet_base_url)
