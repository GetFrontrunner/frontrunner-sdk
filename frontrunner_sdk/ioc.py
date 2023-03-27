from functools import cached_property

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.config import DEFAULT_FRONTRUNNER_CONFIG
from frontrunner_sdk.config import FrontrunnerConfig


class FrontrunnerIoC:

  @property
  def config(self) -> FrontrunnerConfig:
    return DEFAULT_FRONTRUNNER_CONFIG

  @cached_property
  def injective_chain(self) -> InjectiveChain:
    return InjectiveChain()

  @cached_property
  def injective_faucet(self) -> InjectiveFaucet:
    return InjectiveFaucet(self.config.injective_faucet_base_url)
