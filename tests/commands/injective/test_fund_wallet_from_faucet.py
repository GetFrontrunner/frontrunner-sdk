from unittest.mock import MagicMock

from aiohttp.test_utils import AioHTTPTestCase

from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFundWalletFromFaucetOperation(AioHTTPTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  async def test_validate_pass(self):
    req = FundWalletFromFaucetRequest(injective_address="hello")
    cmd = FundWalletFromFaucetOperation(req)
    cmd.validate(self.deps)

  async def test_fund_wallet_from_faucet(self):
    req = FundWalletFromFaucetRequest(injective_address="hello")
    cmd = FundWalletFromFaucetOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsNotNone(res)
