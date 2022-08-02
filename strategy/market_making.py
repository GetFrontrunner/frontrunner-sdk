# get current positions, if program restarted, this will lose all tracked info
# TODO use both perp and spot market to compute variances
from typing import List, Dict, Optional
import datetime
from expiringdict import ExpiringDict


from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network  # , Denom
from pyinjective.composer import Composer
from pyinjective.transaction import Transaction
from pyinjective.wallet import PrivateKey, PublicKey, Address
from pyinjective.utils import (
    derivative_price_from_backend,
    spot_price_from_backend,
    spot_quantity_from_backend,
)

from pyinjective.orderhash import build_eip712_msg, domain_separator
from sha3 import keccak_256 as sha3_keccak_256


from utils.orders import Order, OrderList, compute_order_hashes, get_subaccount_nonce
from utils.markets import factory, Market, ActiveMarket, StagingMarket
from utils.client import build_client, switch_node
from utils.granter import Granter
from utils.utilities import RedisConsumer

# from chain.execution import build_replace_orders_msgs, execute


from asyncio import sleep, get_event_loop
from dotenv import load_dotenv
from configparser import ConfigParser


load_dotenv()


class Model:
    def __init__(
        self,
        configs: ConfigParser,
        private_key: str,
        redis_addr: str,
        fee_recipient: str,
        topics: List[str],
        expire_in: int = 60,
    ):
        self.configs = configs
        self.tob_bid_price = None
        self.tob_ask_price = None
        self.bid_orderbook = None
        self.ask_orderbook = None
        self.position = None
        self.last_trade = None
        self.kline = None
        self.granters: List[Granter] = []  # get_perp_granters(configs, [], n_markets=1)
        self.last_granter_update = 0
        self.consumer = self.get_consumer(redis_addr, topics)

        CONFIG_DIR = "../configs/config_guild_2.ini"
        self.configs.read(CONFIG_DIR)
        self.fee_recipient = fee_recipient
        self.gas_price = 500000000

        nodes = ["sentry0", "sentry1", "sentry3", "k8s"]
        (
            self.node_idx,
            self.network,
            self.composer,
            self.client,
            self.lcd_endpoint,
        ) = build_client(node_idx=3, nodes=nodes)
        self.lcd_endpoint = self.network.lcd_endpoint
        # load account
        self.priv_key: PrivateKey = PrivateKey.from_hex(private_key)
        self.pub_key: PublicKey = self.priv_key.to_public_key()
        self.address = self.pub_key.to_address().init_num_seq(self.network.lcd_endpoint)
        self.inj_address = self.address.to_acc_bech32()
        self.subaccount_id = self.address.get_subaccount_id(index=0)

        self.expire_in = expire_in

    async def on_tob(self, data):
        self.tob_bid_price = data[0]
        self.tob_ask_price = data[0]

    async def on_trade(self, data):
        self.last_trade = data
        print(data)

    async def on_depth(self, data):
        self.bid_orderbook = data["bid"]
        self.ask_orderbook = data["ask"]

    async def on_kline(self, data):
        self.kline = data

    async def on_position(self, data):
        self.position = data

    def get_consumer(
        self, redis_addr: "str" = "127.0.0.1:6379", topics: List[str] = []
    ):
        return RedisConsumer(
            redis_addr,
            topics=topics,
            on_tob=self.on_tob,
            on_trade=self.on_trade,
            on_depth=self.on_depth,
            on_position=self.on_position,
        )

    def update_granters(self):
        pass
        # if self.configs:
        #    self.perp_granters = get_perp_granters(
        #        self.configs, self.perp_granters, n_markets=1
        #    )
        # else:
        #    raise Exception("No config")

    def create_orders_for_granters(self):
        if self.granters:
            for granter in self.granters:
                pass
            self._compute_order_hashes()

            # batch_create_limit_orders_perp(self.signals, perp_granter)

    def _compute_order_hashes(self):
        for granter in self.granters:
            pass
            # batch_compute_order_hashes(granter, self.lcd_endpoint, self.subaccount_id)

    def get_loop(self):
        return get_event_loop()

    async def run(self):
        print("getting data")
        await sleep(30)
        print("slept 30s")
        while True:
            self.update_granters()
            self.create_orders_for_granters()
            # msg = build_replace_orders_msgs(
            #    self.composer,
            #    list(set(self.perp_granters + self.spot_granters)),
            #    self.inj_address,
            # )
            # await execute(
            #    pub_key=self.pub_key,
            #    priv_key=self.priv_key,
            #    address=self.address,
            #    network=self.network,
            #    client=self.client,
            #    composer=self.composer,
            #    gas_price=self.gas_price,
            #    msgs=msg,
            # )
