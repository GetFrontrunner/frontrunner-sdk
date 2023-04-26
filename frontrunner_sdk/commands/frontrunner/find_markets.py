import asyncio

from dataclasses import dataclass
from typing import Collection
from typing import FrozenSet
from typing import Iterable
from typing import Optional
from typing import Set
from typing import Tuple

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api.models.league import League
from frontrunner_sdk.openapi.frontrunner_api.models.market import Market
from frontrunner_sdk.openapi.frontrunner_api.models.prop import Prop
from frontrunner_sdk.openapi.frontrunner_api.models.sport_entity import SportEntity # NOQA
from frontrunner_sdk.openapi.frontrunner_api.models.sport_event import SportEvent # NOQA


@dataclass
class FindMarketsRequest:
  # leagues
  sports: Optional[Iterable[str]]
  league_names: Optional[Iterable[str]]

  # sport events
  event_types: Optional[Iterable[str]]

  # sport entities
  sport_entity_names: Optional[Iterable[str]]
  sport_entity_abbreviations: Optional[Iterable[str]]

  # props
  prop_types: Optional[Iterable[str]]

  # markets
  market_statuses: Optional[Iterable[str]]


@dataclass
class FindMarketsResponse:
  market_ids: Collection[str]
  markets: Iterable[Market]


class FindMarketsOperation(FrontrunnerOperation[FindMarketsRequest, FindMarketsResponse]):

  def __init__(self, request: FindMarketsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  # TODO caching

  @classmethod
  async def find_leagues(
    clz,
    deps: FrontrunnerIoC,
    sports: FrozenSet[str],
    names: FrozenSet[str],
  ) -> Tuple[FrozenSet[str], Iterable[League]]:
    leagues = [
      league for league in await deps.openapi_frontrunner_api.get_leagues()
      if (not sports or league.sport in sports) and (not names or league.name in names)
    ]

    ids = frozenset(league.id for league in leagues)

    return (ids, leagues)

  @classmethod
  async def find_sport_events(
    clz,
    deps: FrontrunnerIoC,
    league_ids: FrozenSet[str],
    event_types: FrozenSet[str],
  ) -> Tuple[FrozenSet[str], Iterable[SportEvent]]:
    sport_events = [
      sport_event for sport_event in await deps.openapi_frontrunner_api.get_sport_events()
      if (sport_event.league_id in league_ids) and (not event_types or sport_event.event_type in event_types)
    ]

    ids = frozenset(sport_event.id for sport_event in sport_events)

    return (ids, sport_events)

  @classmethod
  async def find_sport_entities(
    clz,
    deps: FrontrunnerIoC,
    league_ids: FrozenSet[str],
    names: FrozenSet[str],
    abbreviations: FrozenSet[str],
  ) -> Tuple[FrozenSet[str], Iterable[SportEntity]]:
    sport_entities = [
      sport_entity for sport_entity in await deps.openapi_frontrunner_api.get_sport_entities()
      if (sport_entity.league_id in league_ids) and (not names or sport_entity.name in names) and
      (not abbreviations or sport_entity.abbreviation in abbreviations)
    ]

    ids = frozenset(sport_entity.id for sport_entity in sport_entities)

    return (ids, sport_entities)

  @classmethod
  async def find_props(
    clz,
    deps: FrontrunnerIoC,
    league_ids: FrozenSet[str],
    sport_event_ids: FrozenSet[str],
    prop_types: FrozenSet[str],
  ) -> Tuple[FrozenSet[str], Iterable[Prop]]:
    props = [
      prop for prop in await deps.openapi_frontrunner_api.get_props() if (prop.league_id in league_ids) and
      (prop.sport_event_id in sport_event_ids) and (not prop_types or prop.prop_type in prop_types)
    ]

    ids = frozenset(prop.id for prop in props)

    return (ids, props)

  @classmethod
  async def find_markets(
    clz,
    deps: FrontrunnerIoC,
    sport_entity_ids: Set[str],
    prop_ids: FrozenSet[str],
    statuses: FrozenSet[str],
  ) -> Tuple[FrozenSet[str], Iterable[Market]]:
    markets = [
      market for market in await deps.openapi_frontrunner_api.get_markets()
      if (market.long_entity_id in sport_entity_ids) and (market.prop_id in prop_ids) and
      (not statuses or market.status in statuses)
    ]

    ids = frozenset(market.injective_id for market in markets)

    return (ids, markets)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FindMarketsResponse:
    sports = frozenset(self.request.sports or [])
    league_names = frozenset(self.request.league_names or [])
    event_types = frozenset(self.request.event_types or [])
    sport_entity_names = frozenset(self.request.sport_entity_names or [])
    sport_entity_abbreviations = frozenset(self.request.sport_entity_abbreviations or [])
    prop_types = frozenset(self.request.prop_types or [])
    market_statuses = frozenset(self.request.market_statuses or [])

    league_ids, _ = await self.find_leagues(deps, sports, league_names)

    if not league_ids:
      return FindMarketsResponse(
        market_ids=list([]),
        markets=[],
      )

    (
      (sport_event_ids, _),
      (sport_entity_ids, _),
    ) = await asyncio.gather(
      *[
        self.find_sport_events(deps, league_ids, event_types),
        self.find_sport_entities(deps, league_ids, sport_entity_names, sport_entity_abbreviations),
      ]
    )

    if not sport_event_ids or not sport_entity_ids:
      return FindMarketsResponse(
        market_ids=list([]),
        markets=[],
      )

    prop_ids, _ = await self.find_props(deps, league_ids, sport_event_ids, prop_types)

    if not prop_ids:
      return FindMarketsResponse(
        market_ids=list([]),
        markets=[],
      )

    market_ids, markets = await self.find_markets(deps, sport_entity_ids, prop_ids, market_statuses)

    return FindMarketsResponse(
      market_ids=list(market_ids),
      markets=markets,
    )
