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


class League:
    def __init__(self):
        pass


class SportEntity:
    def __init__(self):
        pass


class SportEvent:
    def __init__(self):
        pass


class Prop:
    def __init__(self):
        pass


class Market:
    def __init__(self):
        pass
