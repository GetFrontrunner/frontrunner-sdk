from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse  # NOQA
from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.injective = InjectiveAsync(self.deps)

    self.wallet = Wallet._new()

  @patch.object(
    FundWalletFromFaucetOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=FundWalletFromFaucetResponse(message="Works"),
  )
  async def test_fund_wallet_from_faucet(self, _execute: AsyncMock):
    await self.injective.fund_wallet_from_faucet(wallet=self.wallet)

    _execute.assert_awaited_once()
