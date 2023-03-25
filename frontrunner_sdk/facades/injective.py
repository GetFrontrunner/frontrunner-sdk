from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.sync import SyncMixin


class InjectiveAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def fund_wallet_from_faucet(self, injective_address: str) -> FundWalletFromFaucetResponse:
    request = FundWalletFromFaucetRequest(injective_address=injective_address)
    return await self._run_operation(FundWalletFromFaucetOperation, self.deps, request)


class Injective(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = InjectiveAsync(deps)

  def fund_wallet_from_faucet(self, injective_address: str) -> FundWalletFromFaucetResponse:
    return self._synchronously(self.impl.fund_wallet_from_faucet, injective_address)
