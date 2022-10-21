from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep
from pickle import dumps

from utils.utilities import RedisProducer

from data.sportsdataio.utilities import *

from data.data_source_template import Data
import xmltodict


class SportsDataIOData(Data):
    def __init__(self, subscription_key: str, redis_addr: str = "127.0.0.1:6379"):
        super().__init__(redis_addr)
        self.url = "https://api.sportsdata.io/v3"
        self.headers.clear()
        self.headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
        }

    async def get_retry(self, topic: str, obj, url: str):

        res = await self.session.get(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    async def post_retry(self, topic: str, obj, url: str):

        res = await self.session.post(url, headers=self.headers)
        if res.status == 200:
            data = await res.text()
            data = obj(data)
            self.redis.produce(topic, dumps(data))
            return True
        else:
            return False

    ############################################################### Sports Data #####################################################################
    async def are_games_in_progress(self, game: str, n=3):
        url = f"{self.url}/{game}/scores/json/AreAnyGamesInProgress"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.json()

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1

    ############################################################### Betting Data #####################################################################
    async def betting_metadata(self, game: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingMetadata"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1

    async def betting_events_by_date(self, game: str, date: str, n=3):
        """
        date = '2020-08-23'
        """
        url = f"{self.url}/{game}/odds/json/BettingEventsByDate/{date}"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1

    async def betting_events_by_season(self, game, season):
        url = f"{self.url}/{game}/odds/json/BettingEvents/{season}"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1
        pass

    async def betting_futures_by_season(self, game, season):
        url = f"{self.url}/{game}/odds/json/BettingFuturesBySeason/{season}"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1
        pass

    async def betting_markets(self, game, market_id):
        url = f"{self.url}/{game}/odds/json/BettingMarket{market_id}"
        topic = ""

        res = await self.session.get(url, heads=self.headers)
        if res.status == 200:
            data = await res.text()
            data_dict = xmltodict.parse(data)

            # recovery_odds = RecoveryOdds(data_dict)
            # self.redis.produce(topic, dumps(recovery_odds))
        else:
            success = False
            logging.info("failed to get recovery odds data from betradar")
            if not success and n > 0:
                # success = await self.post_retry(topic=topic, obj=RecoveryOdds, url=url)
                n -= 1
        pass

    async def betting_markets_by_event(self, game, event_id):
        url = f"{self.url}/{game}/odds/json/BettingMarkets{event_id}"
        pass

    async def betting_markets_by_game_id(self, game, game_id):
        url = f"{self.url}/{game}/odds/json/BettingMarketsByGameID/{game_id}"
        pass

    async def betting_marekts_by_market_type(self, game, event_id, marekt_type_id):
        url = f"{self.url}/{game}/odds/json/BettingMarketsByMarketType/{event_id}/{marekt_type_id}"
        pass

    async def betting_player_props_by_gameid(self, game, game_id):
        url = f"{self.url}/{game}/odds/json/BettingPlayerPropsByGameID/{game_id}"
        pass

    # async def betting_results_by_market(self, game, date):
    async def in_game_odds_by_date(self, game, date):
        url = f"{self.url}/{game}/odds/json/LiveGameOddsByDate/{date}"
        pass

    async def in_game_odds_line_movement(self, game, game_id):
        url = f"{self.url}/{game}/odds/json/LiveGameOddsLineMovement/{game_id}"

    async def period_game_odds_by_date(self, game, date):
        url = f"{self.url}/{game}/odds/json/AlternateMarketGameOddsByDate/{date}"
        pass

    async def period_game_odds_line_movement(self, game, game_id):
        url = (
            f"{self.url}/{game}/odds/json/AlternateMarketGameOddsLineMovement/{game_id}"
        )
        pass

    async def pre_game_odds_by_date(self, game, date):
        url = f"{self.url}/{game}/odds/json/GameOddsByDate/{date}"
        pass

    async def pre_game_odds_line_movement(self, game, game_id):
        url = f"{self.url}/{game}/odds/json/GameOddsLineMovement/{game_id}"
        pass

    async def betting_trends_by_matchup(self, game):
        url = f"{self.url}/{game}/odds/json/"
        pass

    async def sportbooks(self, game):
        url = f"{self.url}/{game}/odds/json/"
        pass

    async def betting_trends_by_team(self, game):
        url = f"{self.url}/{game}/odds/json/ActiveSportsbooks"
        pass

    # async def betting_metadata(self):
    #    pass

    # async def betting_results_by_market(self):
    #    pass

    # async def betting_splits_by_betting_market_id(self):
    #    pass

    # async def betting_splits_by_game_id(self):
    #    pass

    # async def betting_trends_by_matchup(self):
    #    pass

    # async def betting_trends_by_team(self):
    #    pass

    ############################################################### Fantasy Data #####################################################################

    ############################################################### News & Images Data #####################################################################

    ############################################################### Miscellaneous Data #####################################################################
