from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesResponse
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsResponse
from frontrunner_sdk.commands.frontrunner.get_props import GetPropsOperation
from frontrunner_sdk.commands.frontrunner.get_props import GetPropsResponse
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_sports import GetSportsOperation
from frontrunner_sdk.commands.frontrunner.get_sports import GetSportsResponse
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFrontrunnerFacadeAsync(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.facade = FrontrunnerFacadeAsync(self.deps)

  @patch.object(
    FindMarketsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=FindMarketsResponse(
      market_ids=set([]),
      markets=[],
    ),
  )
  async def test_find_markets(self, _execute: AsyncMock):
    await self.facade.find_markets()
    _execute.assert_awaited_once()

  @patch.object(
    GetLeaguesOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetLeaguesResponse(leagues=[],),
  )
  async def test_get_leagues(self, _execute: AsyncMock):
    await self.facade.get_leagues()
    _execute.assert_awaited_once()

  @patch.object(
    GetMarketsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetMarketsResponse(markets=[],),
  )
  async def test_get_markets(self, _execute: AsyncMock):
    await self.facade.get_markets()
    _execute.assert_awaited_once()

  @patch.object(
    GetPropsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetPropsResponse(props=[],),
  )
  async def test_get_props(self, _execute: AsyncMock):
    await self.facade.get_props()
    _execute.assert_awaited_once()

  @patch.object(
    GetSportEntitiesOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetSportEntitiesResponse(sport_entities=[],),
  )
  async def test_get_sport_entities(self, _execute: AsyncMock):
    await self.facade.get_sport_entities()
    _execute.assert_awaited_once()

  @patch.object(
    GetSportEventsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetSportEventsResponse(sport_events=[],),
  )
  async def test_get_sport_events(self, _execute: AsyncMock):
    await self.facade.get_sport_events()
    _execute.assert_awaited_once()

  @patch.object(
    GetSportsOperation,
    "execute",
    new_callable=AsyncMock,
    return_value=GetSportsResponse(sports=[],),
  )
  async def test_get_sports(self, _execute: AsyncMock):
    await self.facade.get_sports()
    _execute.assert_awaited_once()
