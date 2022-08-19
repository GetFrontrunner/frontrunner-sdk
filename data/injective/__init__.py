import logging
from typing import List, Union
from time import time_ns
from math import log
from google.protobuf.json_format import MessageToDict
from orjson import dumps

from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network  # , Denom
from pyinjective.composer import Composer
from pyinjective.transaction import Transaction
from pyinjective.wallet import PrivateKey
from pyinjective.utils import (
    derivative_price_from_backend,
    spot_price_from_backend,
    spot_quantity_from_backend,
)
from pyinjective.orderhash import build_eip712_msg, domain_separator
from sha3 import keccak_256 as sha3_keccak_256

from utils.utilities import RedisProducer, add_message_type
from utils.granter import Granter
from utils.markets import ActiveMarket, StagingMarket
from utils.client import create_client, switch_node_recreate_client


class InjectiveData:
    def __init__(
        self,
        markets: Union[List[ActiveMarket], List[StagingMarket]],
        granters: List[Granter],
        redis_addr: str = "127.0.0.1:6379",
    ):
        self.markets = markets
        self.granters: List[Granter] = granters
        self.nodes = ["sentry0", "sentry1", "sentry3", "k8s"]
        self.node_idx = 3

        (
            self.node_idx,
            self.network,
            self.composer,
            self.client,
            self.lcd_endpoint,
        ) = create_client(self.node_idx, self.nodes)
        self.redis = RedisProducer(redis_addr=redis_addr)

    async def shutdown_client(self):
        await self.client.close_exchange_channel()
        await self.client.close_chain_channel()

    async def shutdown_and_switch_client(self):
        await self.shutdown_client()
        (
            self.node_idx,
            self.network,
            self.composer,
            self.client,
            self.lcd_endpoint,
        ) = switch_node_recreate_client(self.node_idx, self.nodes)

    async def injective_trade_stream(self):
        topic = "Defi/injective_trades"
        while True:
            logging.info("starting injective_trade_stream")
            market_ids = set()
            for market in self.markets:
                market_ids.add(market.market_id)

            if len(market_ids) == 0:
                logging.info("No market to stream for injective trades")
                return

            trades = await self.client.stream_derivative_trades(market_ids=list(market_ids))
            print(market_ids)

            async for trade in trades:
                # print(trade)
                data = MessageToDict(trade)
                data = add_message_type(data, "inj_trade")
                self.redis.produce(topic, dumps(data))
            logging.info("injective trade has been shut down")

    async def injective_orderbook_stream(self):
        topic = "Defi/injective_orderbook"
        while True:
            logging.info("starting injective_orderbook_stream_derivative")
            market_ids = set()
            for market in self.markets:
                market_ids.add(market.market_id)

            logging.info(f"market_ids: {market_ids}")
            if len(market_ids) == 0:
                logging.warning("No market to stream injective orderbook")
                return

            orderbook = await self.client.stream_derivative_orderbooks(market_ids=list(market_ids))

            async for orders in orderbook:
                data = MessageToDict(orders)
                data = add_message_type(data, "inj_orderbook")
                self.redis.produce(topic, dumps(data))
            logging.info("injective orderbook has been shut down")

    async def injective_position_stream(self):
        """
        get subaccount positions from exchange
        entry_price is biased, and restart the bot will lose all local entry
        local entry price is biased, its' always higher than the real entry price
        """
        topic = "Defi/injective_position"
        while True:
            logging.info("starting injective_position_stream")
            market_ids = set()
            for market in self.markets:
                market_ids.add(market.market_id)

            if len(market_ids) == 0:
                logging.warning("No market to stream injective position")
                return

            logging.info(f"market_ids: {market_ids}")

            positions = await self.client.stream_derivative_positions(market_ids=list(market_ids))
            async for position in positions:
                data = MessageToDict(position)
                data = add_message_type(data, "inj_position")
                self.redis.produce(topic, dumps(data))
            logging.info("injective position has been shut down")
