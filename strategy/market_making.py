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


from utils.objects import Order, OrderList
from utils.markets import factory, Market, ActiveMarket, StagingMarket
from utils.client import build_client, switch_node
from utils.granter import Granter
from utils.utilities import RedisConsumer, compute_orderhash, get_nounce


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
        self.granters: List[Granter] = []  # get_perp_granters(configs, [], n_markets=1)
        self.last_granter_update = 0
        self.consumer = self.get_consumer(redis_addr, topics)

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
                bid_price = 0.5
                bid_quantity = 1
                marekt_dict = {"ticker": "staging"}
                market = factory(**marekt_dict)
                granter.create_bid_orders(
                    price=bid_price,
                    quantity=bid_quantity,
                    is_limit=True,
                    market=market,
                    composer=self.composer,
                    lcd_endpoint=self.lcd_endpoint,
                )

                ask_price = 0.5
                ask_quantity = 1
                marekt_dict = {"ticker": "staging"}
                market = factory(**marekt_dict)
                granter.create_ask_orders(
                    price=ask_price,
                    quantity=ask_quantity,
                    is_limit=True,
                    market=market,
                    composer=self.composer,
                    lcd_endpoint=self.lcd_endpoint,
                )

    def batch_replace_order(self):
        msg = self._build_batch_new_orders_msg()

    def batch_new_order(self):
        msg = self._build_batch_new_orders_msg()

    def batch_cancel(self):
        pass

    def _build_batch_replace_orders_msg(self):
        binary_options_orders_to_create = []
        binary_options_orders_to_cancel = []
        binary_options_market_ids_to_cancel_all = []

        for granter in self.granters:
            tmp = (
                [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.limit_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.limit_bids
                ]
                + [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.market_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.market_bids
                ]
            )
            binary_options_orders_to_create.extend(tmp)

        binary_options_market_ids_to_cancel_all = list(
            set([order.market.market_id for order in binary_options_orders_to_create])
        )
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.address.to_acc_bech32(),
            subaccount_id=self.subaccount_id,
            binary_options_orders_to_create=binary_options_orders_to_create,
            binary_options_orders_to_cancel=binary_options_orders_to_cancel,
            binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
        )
        return msg

    def _build_batch_new_orders_msg(self):
        binary_options_orders_to_create = []

        for granter in self.granters:
            tmp = (
                [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.limit_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.limit_bids
                ]
                + [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.market_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.market_bids
                ]
            )
            binary_options_orders_to_create.extend(tmp)

        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.address.to_acc_bech32(),
            subaccount_id=self.subaccount_id,
            binary_options_orders_to_create=binary_options_orders_to_create,
        )
        return msg

    def _build_batch_cancel_all_orders_msg(self):
        binary_options_market_ids_to_cancel_all = []

        for granter in self.granters:
            tmp = (
                [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.limit_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.limit_bids
                ]
                + [
                    ask_order.market.market_id
                    for (orderhash, ask_order) in granter.market_asks
                ]
                + [
                    bid_order.market.market_id
                    for (orderhash, bid_order) in granter.market_bids
                ]
            )
            binary_options_market_ids_to_cancel_all.extend(set(tmp))

        binary_options_market_ids_to_cancel_all = list(
            set(binary_options_market_ids_to_cancel_all)
        )
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.address.to_acc_bech32(),
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
        )
        return msg

    def single_new_order(self):
        pass

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
