from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.models.league import League
from frontrunner_sdk.openapi.frontrunner_api.models.market import Market
from frontrunner_sdk.openapi.frontrunner_api.models.market_status import MarketStatus # NOQA
from frontrunner_sdk.openapi.frontrunner_api.models.prop import Prop
from frontrunner_sdk.openapi.frontrunner_api.models.sport_entity import SportEntity # NOQA
from frontrunner_sdk.openapi.frontrunner_api.models.sport_event import SportEvent # NOQA


class TestFindMarketsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    leagues: Optional[List[League]] = None,
    sport_events: Optional[List[SportEvent]] = None,
    sport_entities: Optional[List[SportEntity]] = None,
    props: Optional[List[Prop]] = None,
    markets: Optional[List[Market]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_leagues = AsyncMock(return_value=leagues or [])
    self.deps.openapi_frontrunner_api.get_sport_events = AsyncMock(return_value=sport_events or [])
    self.deps.openapi_frontrunner_api.get_sport_entities = AsyncMock(return_value=sport_entities or [])
    self.deps.openapi_frontrunner_api.get_props = AsyncMock(return_value=props or [])
    self.deps.openapi_frontrunner_api.get_markets = AsyncMock(return_value=markets or [])

  async def test_find_markets_everything(self):
    self.setup_partner_api(
      leagues=[League(id="league", name="league")],
      sport_events=[SportEvent(id="sport-event", league_id="league", name="sport-event")],
      sport_entities=[SportEntity(id="sport-entity", league_id="league", name="sport-entity")],
      props=[Prop(id="props", league_id="league", sport_event_id="sport-event", name="props")],
      markets=[
        Market(
          id="market",
          injective_id="injective-market",
          long_entity_id="sport-entity",
          prop_id="props",
          status=MarketStatus.ACTIVE
        ),
      ],
    )

    req = FindMarketsRequest(
      sports=[],
      league_names=[],
      event_types=[],
      sport_entity_names=[],
      sport_entity_abbreviations=[],
      prop_types=[],
      market_statuses=[],
    )

    cmd = FindMarketsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.market_ids, ["injective-market"])

  async def test_find_markets_short_circuit(self):
    self.setup_partner_api(leagues=[])

    req = FindMarketsRequest(
      sports=[],
      league_names=[],
      event_types=[],
      sport_entity_names=[],
      sport_entity_abbreviations=[],
      prop_types=[],
      market_statuses=[],
    )

    cmd = FindMarketsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.market_ids, [])

    self.deps.openapi_frontrunner_api.get_markets.assert_not_awaited()
