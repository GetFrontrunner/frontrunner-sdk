from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.injective.create_orders import CreateOrdersOperation  # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersResponse  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletResponse  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetOperation  # NOQA
from frontrunner_sdk.commands.injective.fund_wallet_from_faucet import FundWalletFromFaucetResponse  # NOQA
from frontrunner_sdk.commands.injective.load_wallet_from_mnemonic import LoadWalletFromMnemonicOperation  # NOQA
from frontrunner_sdk.commands.injective.load_wallet_from_mnemonic import LoadWalletFromMnemonicResponse  # NOQA
from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.injective = InjectiveAsync(self.deps)

    self.wallet = Wallet._new()

  @patch.object(
    CreateWalletOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=CreateWalletResponse(wallet=Wallet._new()),
  )
  async def test_create_wallet(self, _execute: AsyncMock):
    await self.injective.create_wallet()
    _execute.assert_awaited_once()

  @patch.object(
    LoadWalletFromMnemonicOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=LoadWalletFromMnemonicResponse(wallet=Wallet._new()),
  )
  async def test_load_wallet_from_mnemonic(self, _execute: AsyncMock):
    mnemonic = Wallet._new().mnemonic
    await self.injective.load_wallet_from_mnemonic(mnemonic)
    _execute.assert_awaited_once()

  @patch.object(
    FundWalletFromFaucetOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=FundWalletFromFaucetResponse(message="Works"),
  )
  async def test_fund_wallet_from_faucet(self, _execute: AsyncMock):
    await self.injective.fund_wallet_from_faucet(self.wallet)
    _execute.assert_awaited_once()

  @patch.object(
    CreateOrdersOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=CreateOrdersResponse(transaction="<hash>"),
  )
  async def test_create_orders(self, _execute: AsyncMock):
    await self.injective.create_orders(self.wallet, [Order.buy_against("<marketid>", 10, 0.7)])
    _execute.assert_awaited_once()
