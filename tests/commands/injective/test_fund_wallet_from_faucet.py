from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetRequest # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestFundWalletFromFaucetOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate_pass(self):
    req = FundWalletFromFaucetRequest(wallet=self.wallet)
    cmd = FundWalletFromFaucetOperation(req)
    cmd.validate(self.deps)

  async def test_fund_wallet_from_faucet(self):
    self.deps.injective_faucet.fund_wallet = AsyncMock(return_value={"message": "Works"})

    req = FundWalletFromFaucetRequest(wallet=self.wallet)
    cmd = FundWalletFromFaucetOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res, FundWalletFromFaucetResponse(message="Works"))
