from datetime import datetime
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsRequest # NOQA
from frontrunner_sdk.commands.frontrunner.find_markets import FindMarketsResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesRequest
from frontrunner_sdk.commands.frontrunner.get_leagues import GetLeaguesResponse
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsRequest
from frontrunner_sdk.commands.frontrunner.get_markets import GetMarketsResponse
from frontrunner_sdk.commands.frontrunner.get_props import GetPropsOperation
from frontrunner_sdk.commands.frontrunner.get_props import GetPropsRequest
from frontrunner_sdk.commands.frontrunner.get_props import GetPropsResponse
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesRequest # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_entities import GetSportEntitiesResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsRequest # NOQA
from frontrunner_sdk.commands.frontrunner.get_sport_events import GetSportEventsResponse # NOQA
from frontrunner_sdk.commands.frontrunner.get_sports import GetSportsOperation
from frontrunner_sdk.commands.frontrunner.get_sports import GetSportsRequest
from frontrunner_sdk.commands.frontrunner.get_sports import GetSportsResponse
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin # NOQA
from frontrunner_sdk.helpers.parameters import as_request_args
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.models.market_status import MarketStatus # NOQA
from frontrunner_sdk.sync import SyncMixin


class FrontrunnerFacadeAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def find_markets(
    self,
    sports: Optional[Iterable[str]] = None,
    league_names: Optional[Iterable[str]] = None,
    event_types: Optional[Iterable[str]] = None,
    sport_entity_names: Optional[Iterable[str]] = None,
    sport_entity_abbreviations: Optional[Iterable[str]] = None,
    prop_types: Optional[Iterable[str]] = None,
    market_statuses: Optional[Iterable[str]] = None,
  ) -> FindMarketsResponse:
    request = FindMarketsRequest(
      sports=sports,
      league_names=league_names,
      event_types=event_types,
      sport_entity_names=sport_entity_names,
      sport_entity_abbreviations=sport_entity_abbreviations,
      prop_types=prop_types,
      market_statuses=market_statuses or [MarketStatus.ACTIVE],
    )

    return await self._run_operation(FindMarketsOperation, self.deps, request)

  async def get_leagues(
    self,
    id: Optional[str] = None,
    sport: Optional[str] = None,
  ) -> GetLeaguesResponse:
    kwargs = as_request_args(locals())
    request = GetLeaguesRequest(**kwargs)
    return await self._run_operation(GetLeaguesOperation, self.deps, request)

  async def get_markets(
    self,
    id: Optional[str] = None,
    injective_id: Optional[str] = None,
    prop_id: Optional[str] = None,
    event_id: Optional[str] = None,
    league_id: Optional[str] = None,
    status: Optional[MarketStatus] = None,
  ) -> GetMarketsResponse:
    kwargs = as_request_args(locals())
    request = GetMarketsRequest(**kwargs)
    return await self._run_operation(GetMarketsOperation, self.deps, request)

  async def get_props(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
  ) -> GetPropsResponse:
    kwargs = as_request_args(locals())
    request = GetPropsRequest(**kwargs)
    return await self._run_operation(GetPropsOperation, self.deps, request)

  async def get_sport_entities(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
    sport: Optional[str] = None,
  ) -> GetSportEntitiesResponse:
    kwargs = as_request_args(locals())
    request = GetSportEntitiesRequest(**kwargs)
    return await self._run_operation(GetSportEntitiesOperation, self.deps, request)

  async def get_sport_events(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
    sport: Optional[str] = None,
    starts_since: Optional[datetime] = None,
  ) -> GetSportEventsResponse:
    kwargs = as_request_args(locals())
    request = GetSportEventsRequest(**kwargs)
    return await self._run_operation(GetSportEventsOperation, self.deps, request)

  async def get_sports(self) -> GetSportsResponse:
    request = GetSportsRequest()
    return await self._run_operation(GetSportsOperation, self.deps, request)


class FrontrunnerFacade(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = FrontrunnerFacadeAsync(deps)

  def find_markets(
    self,
    sports: Optional[Iterable[str]] = None,
    league_names: Optional[Iterable[str]] = None,
    event_types: Optional[Iterable[str]] = None,
    sport_entity_names: Optional[Iterable[str]] = None,
    sport_entity_abbreviations: Optional[Iterable[str]] = None,
    prop_types: Optional[Iterable[str]] = None,
    market_statuses: Optional[Iterable[MarketStatus]] = None,
  ) -> FindMarketsResponse:
    return self._synchronously(
      self.impl.find_markets,
      sports=sports,
      league_names=league_names,
      event_types=event_types,
      sport_entity_names=sport_entity_names,
      sport_entity_abbreviations=sport_entity_abbreviations,
      prop_types=prop_types,
      market_statuses=market_statuses,
    )

  def get_leagues(
    self,
    id: Optional[str] = None,
    sport: Optional[str] = None,
  ) -> GetLeaguesResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_leagues, **kwargs)

  async def get_markets(
    self,
    id: Optional[str] = None,
    injective_id: Optional[str] = None,
    prop_id: Optional[str] = None,
    event_id: Optional[str] = None,
    league_id: Optional[str] = None,
    status: Optional[MarketStatus] = None,
  ) -> GetMarketsResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_markets, **kwargs)

  def get_props(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
  ) -> GetPropsResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_props, **kwargs)

  def get_sport_entities(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
    sport: Optional[str] = None,
  ) -> GetSportEntitiesResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_sport_entities, **kwargs)

  def get_sport_events(
    self,
    id: Optional[str] = None,
    league_id: Optional[str] = None,
    sport: Optional[str] = None,
    starts_since: Optional[datetime] = None,
  ) -> GetSportEventsResponse:
    kwargs = as_request_args(locals())
    return self._synchronously(self.impl.get_sport_events, **kwargs)

  def get_sports(self) -> GetSportsResponse:
    return self._synchronously(self.impl.get_sports)
