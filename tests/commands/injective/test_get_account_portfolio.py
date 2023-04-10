from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioOperation # NOQA
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestCreateWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate(self):
    req = GetAccountPortfolioRequest()
    cmd = GetAccountPortfolioOperation(req)
    cmd.validate(self.deps)

  async def test_create_wallet(self):
    portfolio = MagicMock()
    self.deps.injective_client.get_account_portfolio = AsyncMock(return_value=portfolio)

    req = GetAccountPortfolioRequest()
    cmd = GetAccountPortfolioOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.portfolio, portfolio)

    self.deps.injective_client.get_account_portfolio.assert_awaited_once()
