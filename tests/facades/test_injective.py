from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.injective = InjectiveAsync(self.deps)

  async def test_create_wallet(self):
    response = await self.injective.create_wallet()
    self.assertIsNotNone(response)
