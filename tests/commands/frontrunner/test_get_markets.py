from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsRequest
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api import Market


class TestGetMarketsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    markets: Optional[List[Market]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_markets = AsyncMock(return_value=markets or [])

  async def test_get_markets(self):
    markets = [Market(id="market", injective_id="0x1234", status="active")]
    self.setup_partner_api(markets=markets,)

    req = GetMarketsRequest(id="market",)

    cmd = GetMarketsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.markets, markets)
