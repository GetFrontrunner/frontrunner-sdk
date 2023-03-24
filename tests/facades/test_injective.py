from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.injective import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective import FundWalletFromFaucetResponse  # NOQA
from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.injective = InjectiveAsync(self.deps)

  @patch.object(
    FundWalletFromFaucetOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=FundWalletFromFaucetResponse(
      message="Works",
      injective_address="<fake>",
    ),
  )
  async def test_fund_wallet_from_faucet(self, _execute: AsyncMock):
    await self.injective.fund_wallet_from_faucet(injective_address="<fake>")

    _execute.assert_awaited_once()
