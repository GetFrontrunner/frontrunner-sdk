from unittest import IsolatedAsyncioTestCase

from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestIoC(FrontrunnerIoC):
  pass


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.ioc = TestIoC()
    self.injective = InjectiveAsync(self.ioc)

  async def test_create_wallet(self):
    response = await self.injective.create_wallet()
    self.assertIsNotNone(response)
