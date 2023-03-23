from frontrunner_sdk.commands.injective import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective import CreateWalletRequest  # NOQA
from frontrunner_sdk.commands.injective import CreateWalletResponse  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.sync import SyncMixin


class InjectiveAsync:

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def create_wallet(self) -> CreateWalletResponse:
    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    cmd.validate(self.deps)
    return await cmd.execute(self.deps)


class Injective(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = InjectiveAsync(deps)

  def create_wallet(self) -> CreateWalletResponse:
    return self._synchronously(self.impl.create_wallet)
