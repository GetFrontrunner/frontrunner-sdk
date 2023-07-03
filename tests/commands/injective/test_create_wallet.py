from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestCreateWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate(self):
    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    cmd.validate(self.deps)

  async def test_create_wallet(self):
    self.deps.injective_faucet.fund_wallet = AsyncMock()
    self.deps.use_wallet = AsyncMock()

    req = CreateWalletRequest(fund_and_initialize=True)
    cmd = CreateWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsInstance(res.wallet, Wallet)

    self.deps.injective_faucet.fund_wallet.assert_awaited_once()
    self.deps.use_wallet.assert_awaited_once_with(res.wallet)

  async def test_create_wallet_no_fund_and_init(self):
    self.deps.injective_faucet.fund_wallet = AsyncMock()
    self.deps.use_wallet = AsyncMock()

    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsInstance(res.wallet, Wallet)

    self.deps.injective_faucet.fund_wallet.assert_not_awaited()
    self.deps.use_wallet.assert_not_awaited()
