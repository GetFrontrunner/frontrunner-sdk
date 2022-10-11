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
# from data.matchbook.utilities import *


class Data:
    def __init__(
        self,
        redis_addr: str = "127.0.0.1:6379",
    ):
        self.redis = RedisProducer(redis_addr=redis_addr)
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "api-doc-test-client",
        }

        connector = TCPConnector(keepalive_timeout=1000)
        self.session = ClientSession(
            timeout=ClientTimeout(total=10), headers=self.headers, connector=connector
        )
        self.t = 10
