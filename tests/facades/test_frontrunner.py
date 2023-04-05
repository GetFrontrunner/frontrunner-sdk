from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsResponse # NOQA
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFrontrunnerFacadeAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.facade = FrontrunnerFacadeAsync(self.deps)

  @patch.object(
    ListMarketsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=ListMarketsResponse(markets=[]),
  )
  async def test_create_wallet(self, _execute: AsyncMock):
    await self.facade.list_markets()
    _execute.assert_awaited_once()
