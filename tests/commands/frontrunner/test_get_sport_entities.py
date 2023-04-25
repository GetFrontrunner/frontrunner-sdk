from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api import SportEntity


class TestGetSportEntitiesOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    sport_entities: Optional[List[SportEntity]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_sport_entities = AsyncMock(return_value=sport_entities or [])

  async def test_get_sport_entities(self):
    sport_entities = [SportEntity(id="sport-entity", name="sport-entity-name")]
    self.setup_partner_api(sport_entities=sport_entities,)

    req = GetSportEntitiesRequest(id="sport-entity",)

    cmd = GetSportEntitiesOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.sport_entities, sport_entities)
