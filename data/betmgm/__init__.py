import logging
from typing import Dict, List
from time import time_ns
from math import log
from google.protobuf.json_format import MessageToDict
from orjson import dumps

from utils.utilities import RedisProducer, add_message_type
from utils.granter import Granter
from utils.markets import Market


class BetMGM:
    def __init__(self, markets: List[Market], redis_addr: str = "127.0.0.1:6379"):
        self.markets = markets
        self.redis = RedisProducer(redis_addr=redis_addr)
