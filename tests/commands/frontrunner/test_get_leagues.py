from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesRequest
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.models.league import League


class TestGetLeaguesOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    leagues: Optional[List[League]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_leagues = AsyncMock(return_value=leagues or [])

  async def test_get_leagues(self):
    leagues = [League(id="league", name="league", sport="basketball")]
    self.setup_partner_api(leagues=leagues,)

    req = GetLeaguesRequest(id="league", sport="basketball")

    cmd = GetLeaguesOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.leagues, leagues)
