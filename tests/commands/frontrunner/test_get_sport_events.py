from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api import SportEntity


class TestGetSportEventsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    sport_events: Optional[List[SportEntity]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_sport_events = AsyncMock(return_value=sport_events or [])

  async def test_get_sport_events(self):
    sport_events = [SportEntity(id="sport-event", name="sport-event-name")]
    self.setup_partner_api(sport_events=sport_events,)

    req = GetSportEventsRequest(id="sport-event",)

    cmd = GetSportEventsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.sport_events, sport_events)
