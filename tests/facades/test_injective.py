from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersResponse # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletResponse # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse # NOQA
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioOperation # NOQA
from frontrunner_sdk.commands.injective.get_account_portfolio import GetAccountPortfolioResponse # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksOperation # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksResponse # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsResponse # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesOperation # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesResponse
from frontrunner_sdk.facades.injective import InjectiveFacadeAsync
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveFacadeAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.facade = InjectiveFacadeAsync(self.deps)

  @patch.object(
    CreateWalletOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=CreateWalletResponse(wallet=Wallet._new()),
  )
  async def test_create_wallet(self, _execute: AsyncMock):
    await self.facade.create_wallet()
    _execute.assert_awaited_once()

  @patch.object(
    FundWalletFromFaucetOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=FundWalletFromFaucetResponse(message="Works"),
  )
  async def test_fund_wallet_from_faucet(self, _execute: AsyncMock):
    await self.facade.fund_wallet_from_faucet()
    _execute.assert_awaited_once()

  @patch.object(
    CreateOrdersOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=CreateOrdersResponse(transaction="<hash>"),
  )
  async def test_create_orders(self, _execute: AsyncMock):
    await self.facade.create_orders([Order.buy_against("<marketid>", 10, 0.7)])
    _execute.assert_awaited_once()

  @patch.object(
    CancelAllOrdersOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=CancelAllOrdersResponse(transaction="<hash>"),
  )
  async def test_cancel_all_orders(self, _execute: AsyncMock):
    await self.facade.cancel_all_orders()
    _execute.assert_awaited_once()

  @patch.object(
    GetAccountPortfolioOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetAccountPortfolioResponse(portfolio=MagicMock()),
  )
  async def test_get_account_portfolio(self, _execute: AsyncMock):
    await self.facade.get_account_portfolio()
    _execute.assert_awaited_once()

  @patch.object(
    GetOrderBooksOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetOrderBooksResponse(order_books=MagicMock()),
  )
  async def test_get_order_books(self, _execute: AsyncMock):
    await self.facade.get_order_books(market_ids=["abc"])
    _execute.assert_awaited_once()

  @patch.object(
    GetPositionsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetPositionsResponse(positions=[]),
  )
  async def test_get_positions(self, _execute: AsyncMock):
    await self.facade.get_positions(market_ids=["abc"])
    _execute.assert_awaited_once()

  @patch.object(
    GetTradesOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetTradesResponse(trades=[]),
  )
  async def test_get_trades(self, _execute: AsyncMock):
    await self.facade.get_trades(market_ids=["abc"])
    _execute.assert_awaited_once()
