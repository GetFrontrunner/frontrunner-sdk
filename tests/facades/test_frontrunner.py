from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsResponse # NOQA
from frontrunner_sdk.facades.frontrunner import FrontrunnerAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestInjectiveAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.frontrunner = FrontrunnerAsync(self.deps)

  @patch.object(
    ListMarketsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=ListMarketsResponse(markets=[]),
  )
  async def test_create_wallet(self, _execute: AsyncMock):
    await self.frontrunner.list_markets()
    _execute.assert_awaited_once()
