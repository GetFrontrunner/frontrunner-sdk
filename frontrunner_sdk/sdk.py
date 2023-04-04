from functools import cached_property

from frontrunner_sdk.facades.injective import Injective
from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class FrontrunnerSDKAsync:

  @cached_property
  def dependencies(self):
    return FrontrunnerIoC()

  @cached_property
  def injective(self) -> InjectiveAsync:
    return InjectiveAsync(self.dependencies)


class FrontrunnerSDK:

  @cached_property
  def dependencies(self):
    return FrontrunnerIoC()

  @cached_property
  def injective(self) -> Injective:
    return Injective(self.dependencies)
