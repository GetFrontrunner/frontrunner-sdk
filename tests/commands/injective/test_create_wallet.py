from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletRequest  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestCreateWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate_pass(self):
    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    cmd.validate(self.deps)

  async def test_create_wallet(self):
    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsNotNone(res)
