from functools import cached_property

from frontrunner_sdk.clients import InjectiveChain
from frontrunner_sdk.config import DEFAULT_FRONTRUNNER_CONFIG
from frontrunner_sdk.config import FrontrunnerConfig


class FrontrunnerIoC:

  @property
  def config(self) -> FrontrunnerConfig:
    return DEFAULT_FRONTRUNNER_CONFIG

  @cached_property
  def injective_chain(self) -> InjectiveChain:
    return InjectiveChain()
