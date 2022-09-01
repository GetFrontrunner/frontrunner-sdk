import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep


from typing import List, Union
from time import time_ns
from math import log
from orjson import dumps

from utils.utilities import RedisProducer
from utils.granter import Granter
from utils.markets import ActiveMarket, StagingMarket
from utils.client import create_client, switch_node_recreate_client
from data.matchbook.utilities import *


class MatchbookData:
    def __init__(
        self,
        # markets: Union[List[ActiveMarket], List[StagingMarket]],
        # granters: List[Granter],
        redis_addr: str = "127.0.0.1:6379",
    ):
        # self.markets = markets
        # self.granters = granters
        self.redis = RedisProducer(redis_addr=redis_addr)
        self.url = "https://api.matchbook.com/edge/rest/events/event_id?exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "api-doc-test-client",
        }

        connector = TCPConnector(keepalive_timeout=1000)
        self.session = ClientSession(
            timeout=ClientTimeout(total=10), headers=self.headers, connector=connector
        )

    async def _retry(self, topic: str, obj, url: str) -> bool:
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    async def get_sport(self):
        topic = "Matchbook/sports"
        url = "https://api.matchbook.com/edge/rest/lookups/sports?offset=0&per-page=20&order=name%20asc&status=active"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            sport = Sport(data)
            self.redis.produce(topic, dumps(sport))
        else:
            success = False
            n = 3
            logging.info("failed to get sport data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Sport, url=url)
                n -= 1

    async def get_events(self):
        topic = "Matchbook/events"
        url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            events = Events(data)
            self.redis.produce(topic, dumps(events))
        else:
            success = False
            n = 3
            logging.info("failed to get events data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Events, url=url)
                n -= 1

    async def get_event(self, n=10):
        topic = "Matchbook/event"
        url = "https://api.matchbook.com/edge/rest/events/event_id?exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            event = Event(data)
            self.redis.produce(topic, dumps(event))
        else:
            success = False
            n = 3
            logging.info("failed to get event data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Event, url=url)
                n -= 1

    async def get_markets(self, n=10):
        topic = "Matchbook/markets"
        url = "https://api.matchbook.com/edge/rest/events/event_id/markets?offset=0&per-page=20&states=open%2Csuspended&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            marekts = Markets(data)
            self.redis.produce(topic, dumps(marekts))
        else:
            success = False
            n = 3
            logging.info("failed to get markets data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Markets, url=url)
                n -= 1

    async def get_market(self, n=10):
        topic = "Matchbook/market"
        url = "https://api.matchbook.com/edge/rest/events/event_id/markets/market_id?exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            market = Market(data)
            self.redis.produce(topic, dumps(market))
        else:
            success = False
            n = 3
            logging.info("failed to get market data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Market, url=url)
                n -= 1

    async def get_runners(self, n=10):
        topic = "Matchbook/runners"
        url = "https://api.matchbook.com/edge/rest/events/event_id/markets/market_id/runners?states=open%2Csuspended&include-withdrawn=true&include-prices=true&price-depth=3&price-mode=expanded&exchange-type=back-lay&odds-type=DECIMAL&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            runners = Runners(data)
            self.redis.produce(topic, dumps(runners))
        else:
            success = False
            n = 3
            logging.info("failed to get runners data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Runners, url=url)
                n -= 1

    async def get_runner(self, n=10):
        topic = "Matchbook/runner"
        url = "https://api.matchbook.com/edge/rest/events/event_id/markets/market_id/runners/runner_id?include-prices=false&price-depth=3&price-mode=expanded&exchange-type=back-lay&odds-type=DECIMAL&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            runner = Runner(data)
            self.redis.produce(topic, dumps(runner))
        else:
            success = False
            n = 3
            logging.info("failed to get runner data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_prices(self, n=10):
        topic = "Matchbook/prices"
        url = "https://api.matchbook.com/edge/rest/events/event_id/markets/market_id/runners/runner_id/prices?exchange-type=back-lay&odds-type=DECIMAL&depth=3&price-mode=expanded&exclude-mirrored-prices=false"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            prices = Prices(data)
            self.redis.produce(topic, dumps(prices))
        else:
            success = False
            n = 3
            logging.info("failed to get prices data from matchbook")
            if not success and n > 0:
                success = await self._retry(topic=topic, obj=Prices, url=url)
                n -= 1

    async def close(self):
        if not self.session.closed:
            logging.info("closing session")
            await self.session.close()
        logging.info("closed session")
