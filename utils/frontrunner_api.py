from dataclasses import dataclass
from enum import Enum
import aiohttp
import asyncio


class Frontrunner:
    def __init__(self, *args, **kwargs):
        async def get(self):
            async with aiohttp.ClientSession() as session:
                async with session.get("http://httpbin.org/get") as resp:
                    print(resp.status)
                    print(await resp.text())


class Sport(Enum):
    football = 1
    soccer = 2
    basketball = 3


class MarketStatus(Enum):
    active = 1
    closed = 2


class EventType(Enum):
    game = 1
    future = 2


class PropType(Enum):
    winner = 1
    team_prop = 2
    player_prop = 3
    other = 4


@dataclass(slots=True)
class League:
    id: int
    name: str
    updated: str
    sport: Sport


@dataclass(slots=True)
class SportEntity:
    id: int
    name: str
    abbreviation: str
    updated: str
    league: League


@dataclass(slots=True)
class SportEvent:
    id: int
    name: str
    event_type: EventType
    start_time: str
    created: str
    updated: str
    league: League


@dataclass(slots=True)
class Prop:
    id: int
    name: str
    prop_type: PropType
    created: str
    updated: str
    sport_event: SportEvent


@dataclass(slots=True)
class Market:
    id: int
    injective_id: str
    created: str
    updated: str
    long_entity: SportEntity
    short_entity: SportEntity
    status: MarketStatus
    prop: Prop
