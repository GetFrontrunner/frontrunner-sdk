from unittest import IsolatedAsyncioTestCase

from frontrunner_sdk.commands.injective.create_wallet import CreateWalletOperation  # NOQA
from frontrunner_sdk.commands.injective.create_wallet import CreateWalletRequest  # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestIoC(FrontrunnerIoC):
  pass


class TestCreateWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = TestIoC()

  async def test_create_wallet(self):
    req = CreateWalletRequest()
    cmd = CreateWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsNotNone(res)
