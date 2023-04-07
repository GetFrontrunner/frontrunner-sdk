from functools import cached_property

from frontrunner_sdk.config import DEFAULT
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacade
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.facades.injective import InjectiveFacade
from frontrunner_sdk.facades.injective import InjectiveFacadeAsync
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class FrontrunnerSDKAsync:

  def __init__(self, config: FrontrunnerConfig = DEFAULT):
    self.dependencies = FrontrunnerIoC(config=config)

  @property
  def wallet(self) -> Wallet:
    return self.dependencies.wallet

  @cached_property
  def frontrunner(self) -> FrontrunnerFacadeAsync:
    return FrontrunnerFacadeAsync(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacadeAsync:
    return InjectiveFacadeAsync(self.dependencies)


class FrontrunnerSDK:

  def __init__(self, config: FrontrunnerConfig = DEFAULT):
    self.dependencies = FrontrunnerIoC(config=config)

  @property
  def wallet(self) -> Wallet:
    return self.dependencies.wallet

  @cached_property
  def frontrunner(self) -> FrontrunnerFacade:
    return FrontrunnerFacade(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacade:
    return InjectiveFacade(self.dependencies)
