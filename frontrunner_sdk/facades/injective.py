from frontrunner_sdk.commands.injective import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective import CreateWalletRequest  # NOQA
from frontrunner_sdk.commands.injective import CreateWalletResponse
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.sync import SyncMixin


class InjectiveAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def create_wallet(self) -> CreateWalletResponse:
    return await self._run_operation(CreateWalletOperation, self.deps, CreateWalletRequest())


class Injective(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = InjectiveAsync(deps)

  def create_wallet(self) -> CreateWalletResponse:
    return self._synchronously(self.impl.create_wallet)
