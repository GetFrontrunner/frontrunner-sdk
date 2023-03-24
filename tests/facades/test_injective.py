from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.injective = InjectiveAsync(self.deps)

  async def test_fund_wallet_from_faucet(self):
    response = await self.injective.fund_wallet_from_faucet(injective_address="hello")
    self.assertIsNotNone(response)
