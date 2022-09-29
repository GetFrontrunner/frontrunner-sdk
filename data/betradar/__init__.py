from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep
from pickle import dumps

from utils.utilities import RedisProducer

from data.betradar.utilities import *

from data.data_source_template import Data
import xmltodict
import json


class BetRadarData(Data):
    def __init__(
        self,
        x_access_token: str = "SFtwiihsKUwPqlGIlU",
        redis_addr: str = "127.0.0.1:6379",
    ):
        super().__init__(redis_addr)
        self.url = "https://stgapi.betradar.com/v1"
        self.headers.clear
        self.headers = {
            "accept": "*/*",
            "x-access-token": x_access_token,
        }

    async def get_retry(self, topic: str, obj, url: str):
        if "content-type" in self.headers:
            del self.headers["content-type"]

        res = await self.session.get(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    async def post_retry(self, topic: str, obj, url: str):
        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/x-www-form-urlencoded"

        res = await self.session.post(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    async def recovery_odds(
        self,
        product: str,
        request_id: Optional[int] = None,
        node_id: Optional[int] = None,
        after: Optional[int] = None,
        n: int = 3,
    ) -> None:
        """
        product:
        pre
        liveodds
        premium_cricket
        betpal
        vf
        vbl
        vto
        wns
        vdr
        vhc
        vti
        vci
        vbi
        codds
        """
        if product not in [
            "pre",
            "liveodds",
            "premium_cricket",
            "betpal",
            "vf",
            "vbl",
            "vto",
            "wns",
            "vdr",
            "vhc",
            "vti",
            "vci",
            "vbi",
            "codds",
        ]:
            logging.error("Recovery Odds: Invalid product: %s" % product)
            return

        topic = "BetRadar/recovery_odds"

        url = f"{self.url}/{product}/recovery/initiate_request"

        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/x-www-form-urlencoded"
        params = {}
        if request_id:
            params["request_id"] = request_id
        if node_id:
            params["node_id"] = node_id
        if after:
            params["after"] = after

        res = await self.session.post(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            recovery_odds = RecoveryOdds(data_dict)
            self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1

    async def recovery_all_odds(
        self,
        product: str,
        urn_type: str,
        type_id: int,
        request_id: Optional[int],
        nodes: Optional[int],
        n: int = 3,
    ):
        """
        product:
        'pre',
        'liveodds',
        'premium_cricket',
        'betpal',
        'vf',
        'vbl',
        'vto',
        'vdr',
        'vhc',
        'vti',
        'vci',
        'vbi',
        'codds',

        urn_type:
        'sr:match',
        'sr:stage',
        'sr:tournament',
        'sr:season',
        'vf:match',
        'vbl:match',
        'vto:match',
        'vdr:stage',
        'vhc:stage',
        'vti:match',
        'vci:match',
        'vbi:match',
        'vti:tournament',
        'vci:tournament',
        'vbi:tournament',
        """
        if urn_type not in [
            "sr:match",
            "sr:stage",
            "sr:tournament",
            "sr:season",
            "vf:match",
            "vbl:match",
            "vto:match",
            "vdr:stage",
            "vhc:stage",
            "vti:match",
            "vci:match",
            "vbi:match",
            "vti:tournament",
            "vci:tournament",
            "vbi:tournament",
        ]:
            logging.error("Recovery All Odds: Invalid urn_type")
            return

        if product not in [
            "pre",
            "liveodds",
            "premium_cricket",
            "betpal",
            "vf",
            "vbl",
            "vto",
            "vdr",
            "vhc",
            "vti",
            "vci",
            "vbi",
            "codds",
        ]:
            logging.error("Recovery All Odds: Invalid product")
            return
        topic = "BetRadar/recovery_all_odds"
        url = f"{self.url}/{product}/odds/events/{urn_type}:{type_id}/initiate_request"
        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/x-www-form-urlencoded"
        params = {}
        if request_id:
            params["request_id"] = request_id
        if nodes:
            params["nodes"] = nodes

        res = await self.session.post(url, headers=self.headers, params=params)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            recovery_events = RecoveryEvent(data_dict)
            self.redis.produce(topic, dumps(recovery_events))
        else:
            success = False
            logging.info("failed to get recovery all odds data from betradar")
            if not success and n > 0:
                success = await self.post_retry(topic=topic, obj=RecoveryEvent, url=url)
                n -= 1

    async def recovery_all_statefull_messages(
        self,
        product: str,
        urn_type: str,
        type_id: int,
        request_id: Optional[int],
        node_id: Optional[int],
        n: int = 3,
    ):
        """
        product:
        'pre',
        'liveodds',
        'premium_cricket',
        'betpal',
        'vf',
        'vbl',
        'vto',
        'vdr',
        'vhc',
        'vti',
        'vci',
        'vbi',
        'codds',

        urn_type:
        'sr:match',
        'sr:stage',
        'sr:tournament',
        'sr:season',
        'vf:match',
        'vbl:match',
        'vto:match',
        'vdr:stage',
        'vhc:stage',
        'vti:match',
        'vci:match',
        'vbi:match',
        'vti:tournament',
        'vci:tournament',
        'vbi:tournament',
        """

        if product not in [
            "pre",
            "liveodds",
            "premium_cricket",
            "betpal",
            "vf",
            "vbl",
            "vto",
            "vdr",
            "vhc",
            "vti",
            "vci",
            "vbi",
            "codds",
        ]:
            logging.error("Recovery All Odds: Invalid product")
            return

        if urn_type not in [
            "sr:match",
            "sr:stage",
            "sr:tournament",
            "sr:season",
            "vf:match",
            "vbl:match",
            "vto:match",
            "vdr:stage",
            "vhc:stage",
            "vti:match",
            "vci:match",
            "vbi:match",
            "vti:tournament",
            "vci:tournament",
            "vbi:tournament",
        ]:
            logging.error("Recovery All Odds: Invalid urn_type")
            return

        topic = "BetRadar/recovery_statefull_messages"
        url = f"{self.url}/{product}/stateful_messages/events/{urn_type}:{type_id}/initiate_request"
        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/x-www-form-urlencoded"
        params = {}
        if request_id:
            params["request_id"] = request_id
        if node_id:
            params["node_id"] = node_id

        res = await self.session.post(url, headers=self.headers, params=params)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            recovery_state_msg = RecoveryStateMessage(data_dict)
            self.redis.produce(topic, dumps(recovery_state_msg))
        else:
            success = False
            logging.info("failed to get all stateful messages data from betradar")
            if not success and n > 0:
                success = await self.post_retry(
                    topic=topic, obj=RecoveryStateMessage, url=url
                )
                n -= 1

    async def get_booking_calendar(self, sport_id: int, n: int = 3):
        topic = "BetRadar/booking_calendar"
        url = f"{self.url}/liveodds/booking-calendar/events/sr:match:{sport_id}/book"
        if "content-type" not in self.headers:
            self.headers["content-type"] = "application/x-www-form-urlencoded"

        res = await self.session.post(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            booking_calendar = BookingCalendar(data_dict)
            self.redis.produce(topic, dumps(booking_calendar))
        else:
            success = False
            logging.info("failed to get booking calendar data from betradar")
            if not success and n > 0:
                success = await self.post_retry(
                    topic=topic, obj=BookingCalendar, url=url
                )
                n -= 1

    ################################################################## CustomBet ###################################################################
    async def get_available_selection(self, event_id: int, n: int = 3):
        topic = "BetRadar/available_selection"
        url = f"{self.url}/custombet/sr:match:{event_id}/available_selections"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            available_selection = AvailableSelection(data_dict)
            self.redis.produce(topic, dumps(available_selection))
        else:
            success = False
            logging.info("failed to get custombet data from betradar")
            if not success and n > 0:
                success = await self.get_retry(
                    topic=topic, obj=AvailableSelection, url=url
                )
                n -= 1

    async def get_custombet_probability(self, n: int = 3):
        topic = "BetRadar/custombet_probability"
        url = f"{self.url}/custombet/calculate"

        res = await self.session.post(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            probability = Probability(data_dict)
            self.redis.produce(topic, dumps(probability))
        else:
            success = False
            logging.info("failed to get custombet data from betradar")
            if not success and n > 0:
                success = await self.post_retry(topic=topic, obj=Probability, url=url)
                n -= 1

    async def get_custombet_probability_filter(self, n: int = 3):
        topic = "BetRadar/custombet_probability_filter"
        url = f"{self.url}/custombet/calculate_filter"
        res = await self.session.post(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            probability_filer = Probability(data_dict)
            self.redis.produce(topic, dumps(probability_filer))
        else:
            success = False
            logging.info("failed to get custombet data from betradar")
            if not success and n > 0:
                success = await self.post_retry(topic=topic, obj=Probability, url=url)
                n -= 1

    ################################################################## User Info ###################################################################

    async def get_user_info(self, n: int = 3):
        topic = "BetRadar/user_information"
        url = f"{self.url}/users/whoami.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            user = User(data_dict)
            self.redis.produce(topic, dumps(user))
        else:
            success = False
            logging.info("failed to get user information data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=User, url=url)
                n -= 1

    ################################################################## Probability ###################################################################
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
            data = await res.text()
            data_dict = xmltodict.parse(data)
            probabilities = Probabilities(data_dict)
            self.redis.produce(topic, dumps(probabilities))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Probabilities, url=url)
                n -= 1

    ################################################################## Betting Description ###################################################################
    async def get_markets(self, include_mappings: bool = False, n: int = 3):
        topic = "BetRadar/markets"
        url = f"{self.url}/descriptions/en/markets.xml?include_mappings={str(include_mappings).lower()}"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            markets = Markets(data_dict)
            self.redis.produce(topic, dumps(markets))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Markets, url=url)
                n -= 1

    async def get_void_reasons(self, n: int = 3):
        topic = "BetRadar/void_reasons"
        url = f"{self.url}/descriptions/void_reasons.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            void_reasons = Reasons(data_dict)
            self.redis.produce(topic, dumps(void_reasons))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Reasons, url=url)
                n -= 1

    async def get_betstop_reasons(self, n: int = 3):
        topic = "BetRadar/betstop_reasons"
        url = f"{self.url}/descriptions/betstop_reasons.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            betstop_reasons = Reasons(data_dict)
            self.redis.produce(topic, dumps(betstop_reasons))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Reasons, url=url)
                n -= 1

    async def get_betting_status(self, n: int = 3):
        topic = "BetRadar/betting_status"
        url = f"{self.url}/descriptions/betting_status.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            betting_status = Status(data_dict)
            self.redis.produce(topic, dumps(betting_status))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Status, url=url)
                n -= 1

    async def get_match_status(self, n: int = 3):
        topic = "BetRadar/match_status"
        url = f"{self.url}/descriptions/en/match_status.xml"

        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            match_status = Status(data_dict)
            self.redis.produce(topic, dumps(match_status))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Status, url=url)
                n -= 1

    async def get_market_variant(
        self,
        market_id: int,
        variant_urn: str = "sr:exact_games:bestof:5",
        include_mappings: bool = True,
        product: Optional[str] = None,
        is_direct: bool = True,
        n: int = 3,
    ):
        """
        product:
        pre
        liveodds
        wns
        """
        if product not in ["pre", "liveodds", "wns"]:
            logging.error("Get Market Variant: Invalid product")
            return

        topic = "BetRadar/variant_market"
        if is_direct:
            url = f"{self.url}/{product}/descriptions/en/markets/{market_id}/variants/{variant_urn}"
        else:
            url = f"{self.url}/descriptions/en/markets/{market_id}/variants/{variant_urn}?include_mappings={str(include_mappings).lower()}"

        res = await self.session.get(url)

        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            variant = Variant(data_dict)
            self.redis.produce(topic, dumps(variant))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Variant, url=url)
                n -= 1

    async def get_all_variants(self, n: int = 3):
        topic = "BetRadar/all_variants"
        url = f"{self.url}/descriptions/en/variants.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_variants = Variants(data_dict)
            self.redis.produce(topic, dumps(all_variants))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Variants, url=url)
                n -= 1

    async def get_all_producers(self, n: int = 3):
        topic = "BetRadar/all_producers"
        url = f"{self.url}/descriptions/producers.xml"

    ########################################################  Entity Description  ####################################################################

    async def get_player_profile(self, player_id: int, n: int = 3):
        topic = "BetRadar/player_profile"
        url = f"{self.url}/sports/en/players/sr:player:{player_id}/profile.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            player = Player(data_dict)
            self.redis.produce(topic, dumps(player))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Player, url=url)
                n -= 1

    async def get_competitor(self, urn_type: str, competitior_id: int, n: int = 3):
        """
        urn_type:
        competitor
        simple_team
        """
        topic = "BetRadar/competitor"
        url = f"{self.url}/sports/en/competitors/sr:{urn_type}:{competitior_id}/profile.xml"
        if urn_type not in ["competitor", "simple_team"]:
            logging.info("Get Competitor: urn_type not supported")
            return

        logging.error("Get Market Variant: Invalid product")
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            competitors = Competitors(data_dict)
            self.redis.produce(topic, dumps(competitors))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Competitors, url=url)
                n -= 1

    async def get_venue(self, venue_id: int, n: int = 3):
        topic = "BetRadar/venue"
        url = f"{self.url}/sports/en/venues/sr:venue:{venue_id}/profile.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            venues = Venues(data_dict)
            self.redis.produce(topic, dumps(venues))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Venues, url=url)
                n -= 1

    ########################################################  Sport Event Info  ####################################################################
    async def get_sport_event_summary(self, urn_type: str, event_id: int, n: int = 3):
        """
        urn_type:
        'sr:match',
        'sr:stage',
        'sr:season',
        'sr:tournament',
        'sr:simple_tournament',
        'vf:match',
        'vf:season',
        'vf:tournament',
        'vbl:match',
        'vbl:season',
        'vbl:tournament',
        'vto:season',
        'vto:match',
        'vto:tournament',
        'vdr:stage',
        'vhc:stage',
        'vti:match',
        'vti:tournament',
        'vci:match',
        'vci:tournament',
        'vbi:match',
        'vbi:tournament',
        """
        topic = "BetRadar/event_summary"
        url = f"{self.url}/sports/en/sport_events/{urn_type}:{event_id}/summary.xml"
        if urn_type not in [
            "sr:match",
            "sr:stage",
            "sr:season",
            "sr:tournament",
            "sr:simple_tournament",
            "vf:match",
            "vf:season",
            "vf:tournament",
            "vbl:match",
            "vbl:season",
            "vbl:tournament",
            "vto:season",
            "vto:match",
            "vto:tournament",
            "vdr:stage",
            "vhc:stage",
            "vti:match",
            "vti:tournament",
            "vci:match",
            "vci:tournament",
            "vbi:match",
            "vbi:tournament",
        ]:
            logging.error("Get Sport Event Summary: Invalid urn type")
            return
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            summary = Summary(data_dict)
            self.redis.produce(topic, dumps(summary))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Summary, url=url)
                n -= 1

    async def get_event_info(self, urn_type: str, event_id: int, n: int = 3):
        """
        urn_type:
        sr:match
        sr:stage
        """
        if urn_type not in ["sr:match", "sr:stage"]:
            logging.error("Get Event Info: Invalid urn type")
            return
        topic = "BetRadar/event_info"
        url = f"{self.url}/sports/en/sport_events/sr:{urn_type}:{event_id}/timeline.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            events = Events(data_dict)
            self.redis.produce(topic, dumps(events))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Events, url=url)
                n -= 1

    async def get_all_sport_categories(self, sport_id: int, n: int = 3):
        topic = "BetRadar/sport_categories"
        url = f"{self.url}/sports/en/sports/sr:sport:{sport_id}/categories.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            categories = Categories(data_dict)
            self.redis.produce(topic, dumps(categories))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Categories, url=url)
                n -= 1

    async def get_all_sport_tournaments(self, sport_id: int, n: int = 3):
        topic = "BetRadar/sport_tournaments"
        url = f"{self.url}/sports/en/sports/sr:sport:{sport_id}/tournaments.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_sport_tournaments = Tournaments(data_dict)
            self.redis.produce(topic, dumps(all_sport_tournaments))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Tournaments, url=url)
                n -= 1

    async def get_all_sports(self, n: int = 3):
        topic = "BetRadar/sports"
        url = f"{self.url}/sports/en/sports.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_sports = Sports(data_dict)
            self.redis.produce(topic, dumps(all_sports))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Sports, url=url)
                n -= 1

    async def get_all_tournaments(self, n: int = 3):
        topic = "BetRadar/tournaments"
        url = f"{self.url}/sports/en/tournaments.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_tournaments = Tournaments(data_dict)
            self.redis.produce(topic, dumps(all_tournaments))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Tournaments, url=url)
                n -= 1

    async def get_info(self, urn_type: str, tournament_id: int, n: int = 3):
        """
        urn_type:
        'sr:tournament',
        'sr:season',
        'sr:stage',
        'sr:simple_tournament',
        'vf:tournament',
        'vf:season',
        'vbl:tournament',
        'vbl:season',
        'vto:tournament',
        'vto:season',
        'vdr:stage',
        'vhc:stage',
        'vti:tournament',
        'vci:tournament',
        'vbi:tournament',
        """
        if urn_type in [
            "sr:tournament",
            "sr:season",
            "sr:stage",
            "sr:simple_tournament",
            "vf:tournament",
            "vf:season",
            "vbl:tournament",
            "vbl:season",
            "vto:tournament",
            "vto:season",
            "vdr:stage",
            "vhc:stage",
            "vti:tournament",
            "vci:tournament",
            "vbi:tournament",
        ]:
            logging.error("Get Info: Invalid urn_type")
            return
        topic = "BetRadar/info"
        url = f"{self.url}/sports/en/tournaments/sr:{urn_type}:{tournament_id}/info.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            info = Info(data_dict)
            self.redis.produce(topic, dumps(info))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Info, url=url)
                n -= 1

    async def get_all_seasons(self, urn_type: str, tournament_id: int, n: int = 3):
        """
        urn_type:
        season
        tournaments
        """
        topic = "BetRadar/seasons"
        url = f"{self.url}/sports/en/tournaments/sr:{urn_type}:{tournament_id}/seasons.xml"
        if urn_type not in ["season", "tournaments"]:
            logging.error("Get All Seasons: invalid urn_type")
            return
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            seasons = Seasons(data_dict)
            self.redis.produce(topic, dumps(seasons))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Seasons, url=url)
                n -= 1

    ####################################################                    ###################################################################

    async def get_sport_fixture(self, urn_type: str, event_id: int, n: int = 3):
        topic = "BetRadar/sport_fixture"
        url = f"{self.url}/sports/en/sport_events/{urn_type}:{event_id}/fixture.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            fixtures = Fixture(data_dict)
            self.redis.produce(topic, dumps(fixtures))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Fixture, url=url)
                n -= 1

    async def get_sport_schedule(self, date: str, n: int = 3):
        topic = "BetRadar/sport_schedule"
        url = f"{self.url}/sports/en/schedules/{date}/schedule.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            sport_schedule = Schedules(data_dict)
            self.redis.produce(topic, dumps(sport_schedule))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Schedules, url=url)
                n -= 1

    async def get_live_schedule(self, n: int = 3):
        topic = "BetRadar/live_schedule"
        url = f"{self.url}/sports/en/schedules/live/schedule.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            live_schedules = Schedules(data_dict)
            self.redis.produce(topic, dumps(live_schedules))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Schedules, url=url)
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
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_schedules = Schedules(data_dict)
            self.redis.produce(topic, dumps(all_schedules))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Schedules, url=url)
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
            data = await res.text()
            data_dict = xmltodict.parse(data)
            tournament_schedules = Schedules(data_dict)
            self.redis.produce(topic, dumps(tournament_schedules))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=Schedules, url=url)
                n -= 1

    async def get_fixture_changes(self, n: int = 3):
        topic = "BetRadar/fixture_changes"
        url = f"{self.url}/sports/en/fixtures/changes.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            fixture_changes = FixtureChanges(data_dict)
            self.redis.produce(topic, dumps(fixture_changes))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=FixtureChanges, url=url)
                n -= 1

    async def get_all_fixture_changes(self, n: int = 3):
        topic = "BetRadar/all_fixture_changes"
        url = f"{self.url}/sports/en/results/changes.xml"
        res = await self.session.get(url)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)
            all_fixture_changes = ResultsChanges(data_dict)
            self.redis.produce(topic, dumps(all_fixture_changes))
        else:
            success = False
            logging.info("failed to get probabilities data from betradar")
            if not success and n > 0:
                success = await self.get_retry(topic=topic, obj=ResultsChanges, url=url)
                n -= 1
