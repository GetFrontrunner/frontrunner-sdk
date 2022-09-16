from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep
from pickle import dumps

from utils.utilities import RedisProducer

# from utils.granter import Granter
# from utils.markets import ActiveMarket, StagingMarket
# from utils.client import create_client, switch_node_recreate_client
from data.betradar.utilities import *
from data.data_source_template import Data


class BetRadarData(Data):
    def __init__(
        self,
        redis_addr: str = "127.0.0.1:6379",
    ):
        super().__init__(redis_addr)
        self.url = f"https://api.betradar.com/v1"
        self.headers.clear

    async def _retry(self, topic: str, obj, url: str):
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    async def recovery_odds(self, product: str, request_id: int, n: int = 3) -> None:
        topic = "BetRadar/recovery_odds"
        url = f"{self.url}/{product}/recovery/initiate_request?request_id={request_id}"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def recovery_all_odds(
        self, product: str, urn_type: str, type_id: int, request_id: int, n: int = 3
    ):
        topic = "BetRadar/recovery_all_odds"
        url = f"{self.url}/{product}/odds/events/{urn_type}:{type_id}/initiate_request?request_id={request_id}"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get recovery all odds data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def recovery_all_statefull_messages(
        self, product: str, urn_type: str, type_id: int, request_id: int, n: int = 3
    ):
        topic = "BetRadar/recovery_statefull_messages"
        url = f"{self.url}/{product}/stateful_messages/events/{urn_type}:{type_id}/initiate_request?request_id={request_id}"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get all stateful messages data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_booking_calendar(self, sport_id: int, n: int = 3):
        topic = "BetRadar/booking_calendar"
        url = f"{self.url}/liveodds/booking-calendar/events/sr:match:{sport_id}/book"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get booking calendar data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_custombet_probability(self, n: int = 3):
        topic = "BetRadar/custombet_probability"
        url = f"{self.url}/custombet/calculate"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get custombet data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_custombet_probability_filter(self, n: int = 3):
        topic = "BetRadar/custombet_probability_filter"
        url = f"{self.url}/custombet/calculate_filter"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get custombet data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_user_info(self, n: int = 3):
        topic = "BetRadar/user_information"
        url = f"{self.url}/users/whoami.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get user information data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_probabilities(
        self,
        urn_type: str,
        type_id: int,
        market_id: Optional[int] = None,
        specifier: Optional[str] = None,
        n: int = 3,
    ):
        topic = "BetRadar/probabilities"
        if market_id is None and specifier is None:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}"
        elif specifier is None:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}/{market_id}"
        else:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}/{market_id}/{specifier}"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_markets(self, include_mappings: bool = False, n: int = 3):
        topic = "BetRadar/markets"
        url = f"{self.url}/descriptions/en/markets.xml?include_mappings={str(include_mappings).lower()}"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_void_reasons(self, n: int = 3):
        topic = "BetRadar/void_reasons"
        url = f"{self.url}/descriptions/void_reasons.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_betstop_reasons(self, n: int = 3):
        topic = "BetRadar/betstop_reasons"
        url = f"{self.url}/descriptions/betstop_reasons.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_betting_status(self, n: int = 3):
        topic = "BetRadar/betting_status"
        url = f"{self.url}/descriptions/betting_status.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_match_status(self, n: int = 3):
        topic = "BetRadar/match_status"
        url = f"{self.url}/descriptions/en/match_status.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_market_variant(
        self,
        market_id: int,
        variant_urn: str = "sr:exact_games:bestof:5",
        include_mappings: bool = True,
        n: int = 3,
    ):
        topic = "BetRadar/variance_market"
        url = f"{self.url}/descriptions/en/markets/{market_id}/variants/{variant_urn}?include_mappings={str(include_mappings).lower()}"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_product_market_variant(
        self,
        product: str,
        market_id: int,
        variant_urn: str = "sr:exact_games:bestof:5",
        n: int = 3,
    ):
        topic = "BetRadar/product_variance_market"
        url = f"{self.url}/{product}/descriptions/en/markets/{market_id}/variants/{variant_urn}"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_variants(self, n: int = 3):
        topic = "BetRadar/all_variants"
        url = f"{self.url}/descriptions/en/variants.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_producers(self, n: int = 3):
        topic = "BetRadar/all_producers"
        url = f"{self.url}/descriptions/producers.xml"

    async def get_player_profile(self, player_id: int, n: int = 3):
        topic = "BetRadar/player_profile"
        url = f"{self.url}/sports/en/players/sr:player:{player_id}/profile.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_competitor(self, urn_type: str, competitior_id: int, n: int = 3):
        topic = "BetRadar/competitor"
        url = f"{self.url}/sports/en/competitors/sr:{urn_type}:{competitior_id}/profile.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_venue(self, venue_id: int, n: int = 3):
        topic = "BetRadar/venue"
        url = f"{self.url}/sports/en/venues/sr:venue:{venue_id}/profile.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_sport_event_summary(self, urn_type: str, event_id: int, n: int = 3):
        topic = "BetRadar/event_summary"
        url = f"{self.url}/sports/en/sport_events/{urn_type}:{event_id}/summary.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_event_info(self, urn_type: str, event_id: int, n: int = 3):
        topic = "BetRadar/event_info"
        url = f"{self.url}/sports/en/sport_events/sr:{urn_type}:{event_id}/timeline.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_sport_categories(self, sport_id: int, n: int = 3):
        topic = "BetRadar/sport_categories"
        url = f"{self.url}/sports/en/sports/sr:sport:{sport_id}/categories.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_sport_tournaments(self, sport_id: int, n: int = 3):
        topic = "BetRadar/sport_tournaments"
        url = f"{self.url}/sports/en/sports/sr:sport:{sport_id}/tournaments.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_sports(self, n: int = 3):
        topic = "BetRadar/sports"
        url = f"{self.url}/sports/en/sports.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_tournaments(self, n: int = 3):
        topic = "BetRadar/tournaments"
        url = f"{self.url}/sports/en/tournaments.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_info(self, urn_type: str, tournament_id: int, n: int = 3):
        topic = "BetRadar/info"
        url = f"{self.url}/sports/en/tournaments/sr:{urn_type}:{tournament_id}/info.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_seasons(self, urn_type: str, tournament_id: int, n: int = 3):
        topic = "BetRadar/seasons"
        url = f"{self.url}/sports/en/tournaments/sr:{urn_type}:{tournament_id}/seasons.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_sport_fixture(self, urn_type: str, event_id: int, n: int = 3):
        topic = "BetRadar/sport_fixture"
        url = f"{self.url}/sports/en/sport_events/{urn_type}:{event_id}/fixture.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_sport_schedule(self, date: str, n: int = 3):
        topic = "BetRadar/sport_schedule"
        url = f"{self.url}/sports/en/schedules/{date}/schedule.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_live_schedule(self, n: int = 3):
        topic = "BetRadar/live_schedule"
        url = f"{self.url}/sports/en/schedules/live/schedule.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_schedules(self, start: int, n: int = 3):
        """
        Lists almost all events we are offering prematch odds for. This endpoint can be used during early startup to obtain almost all fixtures. This endpoint is one of the few that uses pagination. xml schema
        """
        topic = "BetRadar/all_schedules"
        url = (
            f"{self.url}/sports/en/schedules/pre/schedule.xml?start={start}&limit=1000"
        )
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_tournament_schedule(
        self, urn_type: str, tournament_id: int, n: int = 3
    ):
        topic = "BetRadar/tournament_schedule"
        url = (
            f"{self.url}/sports/en/tournaments/{urn_type}:{tournament_id}/schedule.xml"
        )
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_fixture_changes(self, n: int = 3):
        topic = "BetRadar/fixture_changes"
        url = f"{self.url}/sports/en/fixtures/changes.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1

    async def get_all_fixture_changes(self, n: int = 3):
        topic = "BetRadar/all_fixture_changes"
        url = f"{self.url}/sports/en/results/changes.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.json()
            # runner = Runner(data)
            # self.redis.produce(topic, dumps(runner))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                # success = await self._retry(topic=topic, obj=Runner, url=url)
                n -= 1
