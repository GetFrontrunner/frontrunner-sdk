from functools import cached_property
from frontrunner_sdk.config import DEFAULT

from frontrunner_sdk.facades.frontrunner import FrontrunnerFacade
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.facades.injective import InjectiveFacade
from frontrunner_sdk.facades.injective import InjectiveFacadeAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class FrontrunnerSDKAsync:

  @cached_property
  def dependencies(self):
    return FrontrunnerIoC(DEFAULT)

  @cached_property
  def frontrunner(self) -> FrontrunnerFacadeAsync:
    return FrontrunnerFacadeAsync(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacadeAsync:
    return InjectiveFacadeAsync(self.dependencies)


class FrontrunnerSDK:

  @cached_property
  def dependencies(self):
    return FrontrunnerIoC(DEFAULT)

  @cached_property
  def frontrunner(self) -> FrontrunnerFacade:
    return FrontrunnerFacade(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacade:
    return InjectiveFacade(self.dependencies)
