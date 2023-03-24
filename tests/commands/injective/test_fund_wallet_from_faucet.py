from unittest import IsolatedAsyncioTestCase
from unittest import skip
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFundWalletFromFaucetOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  async def test_validate_pass(self):
    req = FundWalletFromFaucetRequest(injective_address="hello")
    cmd = FundWalletFromFaucetOperation(req)
    cmd.validate(self.deps)

  @skip("no mock for real request yet")
  async def test_fund_wallet_from_faucet(self):
    req = FundWalletFromFaucetRequest(injective_address="hello")
    cmd = FundWalletFromFaucetOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsNotNone(res)
