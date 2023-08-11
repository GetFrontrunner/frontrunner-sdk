from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from frontrunner_sdk.commands.injective.refresh_wallet import RefreshWalletRequest # NOQA
from frontrunner_sdk.commands.injective.refresh_wallet import RefreshWalletOperation # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestCreateWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()

    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.deps.wallet = AsyncMock(return_value=self.wallet)

    self.deps.injective_light_client_daemon.initialize_wallet = AsyncMock()

  async def test_refresh_wallet(self):
    req = RefreshWalletRequest()
    cmd = RefreshWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.deps.injective_light_client_daemon.initialize_wallet.assert_awaited_once_with(self.wallet)

    self.assertIs(res.wallet, self.wallet)
