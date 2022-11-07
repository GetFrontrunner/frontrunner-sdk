from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep
from pickle import dumps

from utils.utilities import RedisProducer

from data.sportsdataio.utilities.betting_data import *

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
        topic = f"{game}/are_games_in_progress"

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
        topic = f"{game}/betting_metadata"

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
        topic = f"{game}/betting_events_by_date"

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

    async def betting_events_by_season(self, game: str, season: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingEvents/{season}"
        topic = f"{game}/betting_events_by_season"

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

    async def betting_futures_by_season(self, game: str, season: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingFuturesBySeason/{season}"
        topic = f"{game}/betting_futures_by_season"

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

    async def betting_markets(self, game: str, market_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingMarket{market_id}"
        topic = f"{game}/betting_markets"

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

    async def betting_markets_by_event(self, game: str, event_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingMarkets{event_id}"
        topic = f"{game}/betting_markets_by_event"

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

    async def betting_markets_by_game_id(self, game: str, game_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingMarketsByGameID/{game_id}"
        topic = f"{game}/betting_markets_by_game_id"

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

    async def betting_marekts_by_market_type(
        self, game: str, event_id: str, marekt_type_id: str, n=3
    ):
        url = f"{self.url}/{game}/odds/json/BettingMarketsByMarketType/{event_id}/{marekt_type_id}"
        topic = f"{game}/betting_markets_by_market_type"

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

    async def betting_player_props_by_gameid(self, game: str, game_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/BettingPlayerPropsByGameID/{game_id}"
        topic = f"{game}/betting_player_props_by_gameid"

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

    # async def betting_results_by_market(self, game, date):
    async def in_game_odds_by_date(self, game: str, date: str, n=3):
        url = f"{self.url}/{game}/odds/json/LiveGameOddsByDate/{date}"
        topic = f"{game}/in_game_odds_by_date"

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

    async def in_game_odds_line_movement(self, game: str, game_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/LiveGameOddsLineMovement/{game_id}"
        topic = f"{game}/in_game_odds_line_movement"

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

    async def period_game_odds_by_date(self, game: str, date: str, n=3):
        url = f"{self.url}/{game}/odds/json/AlternateMarketGameOddsByDate/{date}"
        topic = f"{game}/period_game_odds_by_date"

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

    async def period_game_odds_line_movement(self, game: str, game_id: str, n=3):
        url = (
            f"{self.url}/{game}/odds/json/AlternateMarketGameOddsLineMovement/{game_id}"
        )
        topic = f"{game}/period_game_odds_line_movement"

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

    async def pre_game_odds_by_date(self, game: str, date: str, n=3):
        url = f"{self.url}/{game}/odds/json/GameOddsByDate/{date}"
        topic = f"{game}/pre_game_odds_by_date"

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

    async def pre_game_odds_line_movement(self, game: str, game_id: str, n=3):
        url = f"{self.url}/{game}/odds/json/GameOddsLineMovement/{game_id}"
        topic = f"{game}/pre_game_odds_line_movement"

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

    async def betting_trends_by_matchup(self, game: str, n=3):
        url = f"{self.url}/{game}/odds/json/"
        topic = f"{game}/betting_trends_by_matchup"

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

    async def sportbooks(self, game: str, n=3):
        url = f"{self.url}/{game}/odds/json/"
        topic = f"{game}/sportbooks"

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

    async def betting_trends_by_team(self, game: str, n=3):
        url = f"{self.url}/{game}/odds/json/ActiveSportsbooks"
        topic = f"{game}/betting_trends_by_team"

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
    async def dfs_slates_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/projections/json/DfsSlatesByDate/{date}"
        topic = f"{game}/dfs_slates_by_date"

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

    async def projected_player_games_stats_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/projections/json/PlayerGameProjectionStatsByDate/{date} "
        topic = f"{game}/projected_player_games_stats_by_date"

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

    async def projected_player_season_stats(self, game:str,season: str, n=3):
        url = f"{self.url}/{game}/projections/json/PlayerSeasonProjectionStats/{season} "
        topic = f"{game}/projected_player_season_stats"

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

    async def starting_lineups_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/projections/json/StartingLineupsByDate/{date}"
        topic = f"{game}/starting_lineups_by_date"

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

    async def depth_charts(self,game:str, n=3):
        url = f"{self.url}/{game}/projections/json/DepthCharts "
        topic = f"{game}/depth_charts"

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

    ############################################################### News & Images Data #####################################################################
    async def premium_news(self,game:str, n=3):
        url = f"{self.url}/{game}/news-rotoballer/json/RotoBallerPremiumNews"
        topic = f"{game}/premium_news"

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

    async def premium_news_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/news-rotoballer/json/RotoBallerPremiumNewsByDate/{date}"
        topic = f"{game}/premium_news_by_date"

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

    async def premium_news_by_player(self,game:str, playerid: int, n=3):
        url = f"{self.url}/{game}/news-rotoballer/json/RotoBallerPremiumNewsByPlayerID/{playerid}"
        topic = f"{game}/premium_news_by_player"

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

    async def rotoworld_player_news_recent(self, game:str,n=3):
        url = f"{self.url}/{game}/rotoworld/json/RotoworldPlayerNews"
        topic = f"{game}/rotoworld_player_news_recent"

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

    async def rotoworld_player_news_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/rotoworld/json/RotoworldPlayerNewsByDate/{date}"
        topic = f"{game}/rotoworld_player_news_by_date"

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

    async def headshots(self,game:str, n=3):
        url = f"{self.url}/{game}/headshots/json/Headshots"
        topic = f"{game}/headshots"

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

    ############################################################### Miscellaneous Data #####################################################################
    async def news(self, game:str, n=3):
        url = f"{self.url}/{game}/scores/json/News"
        topic = f"{game}/news"

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

    async def news_by_date(self, game:str,date: str, n=3):
        url = f"{self.url}/{game}/scores/json/NewsByDate/{date}"
        topic = f"{game}/news_by_date"

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

    async def news_by_player(self, game:str,playerid: int, n=3):
        url = f"{self.url}/{game}/scores/json/NewsByPlayerID/{playerid}"
        topic = f"{game}/news_by_player"

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
