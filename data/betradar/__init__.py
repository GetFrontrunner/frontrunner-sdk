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

    async def recovery_odds(self, product: str, request_id: int) -> None:
        topic = "BetRadar/recovery_odds"
        url = f"{self.url}/{product}/recovery/initiate_request?request_id={request_id}"

    async def get_all_odds(
        self, product: str, urn_type: str, type_id: int, request_id: int
    ):
        topic = "BetRadar/all_odds"
        url = f"{self.url}/{product}/odds/events/{urn_type}:{type_id}/initiate_request?request_id={request_id}"

    async def get_all_statefull_messages(
        self, product: str, urn_type: str, type_id: int, request_id: int
    ):
        topic = "BetRadar/statefull_messages"
        url = f"{self.url}/{product}/stateful_messages/events/{urn_type}:{type_id}/initiate_request?request_id={request_id}"

    async def get_booking_calendar(self, sport_id: int):
        topic = "BetRadar/booking_calendar"
        url = f"{self.url}/liveodds/booking-calendar/events/sr:match:{sport_id}/book"

    async def get_custombet_probability(self):
        topic = "BetRadar/custombet_probability"
        url = f"{self.url}/custombet/calculate"

    async def get_custombet_probability_filter(self):
        topic = "BetRadar/custombet_probability_filter"
        url = f"{self.url}/custombet/calculate_filter"

    async def get_user_info(self):
        topic = "BetRadar/user_information"
        url = f"{self.url}/users/whoami.xml"

    async def get_probabilities(
        self,
        urn_type: str,
        type_id: int,
        market_id: Optional[int] = None,
        specifier: Optional[str] = None,
    ):
        topic = "BetRadar/probabilities"
        if market_id is None and specifier is None:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}"
        elif specifier is None:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}/{market_id}"
        else:
            url = f"{self.url}/v1/probabilities/{urn_type}:{type_id}/{market_id}/{specifier}"
