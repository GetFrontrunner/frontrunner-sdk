from functools import cached_property

from frontrunner_sdk.config import DEFAULT
from frontrunner_sdk.config.base import FrontrunnerConfig
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacade
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.facades.injective import InjectiveFacade
from frontrunner_sdk.facades.injective import InjectiveFacadeAsync
from frontrunner_sdk.facades.utilities import UtilitiesFacade
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet
from frontrunner_sdk.sync import SyncMixin


class FrontrunnerSDKAsync:

  def __init__(self, config: FrontrunnerConfig = DEFAULT):
    self.dependencies = FrontrunnerIoC(config=config)

  async def wallet(self) -> Wallet:
    return await self.dependencies.wallet()

  @cached_property
  def frontrunner(self) -> FrontrunnerFacadeAsync:
    return FrontrunnerFacadeAsync(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacadeAsync:
    return InjectiveFacadeAsync(self.dependencies)

  @cached_property
  def utilities(self) -> UtilitiesFacade:
    return UtilitiesFacade(self.dependencies)


class FrontrunnerSDK(SyncMixin):

  def __init__(self, config: FrontrunnerConfig = DEFAULT):
    self.dependencies = FrontrunnerIoC(config=config)

  def wallet(self) -> Wallet:
    return self._synchronously(self.dependencies.wallet)

  @cached_property
  def frontrunner(self) -> FrontrunnerFacade:
    return FrontrunnerFacade(self.dependencies)

  @cached_property
  def injective(self) -> InjectiveFacade:
    return InjectiveFacade(self.dependencies)

  @cached_property
  def utilities(self) -> UtilitiesFacade:
    return UtilitiesFacade(self.dependencies)
