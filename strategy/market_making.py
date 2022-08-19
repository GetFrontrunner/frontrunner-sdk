# get current positions, if program restarted, this will lose all tracked info
# TODO use both perp and spot market to compute variances
import os
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

from utils.markets import binary_states_market_factory  # , Market, ActiveMarket, StagingMarket

from utils.binary_state_market_granter import BinaryStateGranter
from utils.get_markets import get_all_active_markets, get_all_staging_markets
from utils.utilities import RedisConsumer, get_nonce
from utils.objects import Order, Probability, Probabilities, Event
from utils.markets import Market, ActiveMarket, StagingMarket
from chain.execution import execute
from chain.client import create_client, switch_node_recreate_client
import logging

from asyncio import sleep, get_event_loop
from dotenv import load_dotenv
from configparser import ConfigParser


load_dotenv()


class Model:
    def __init__(
        self,
        # configs: ConfigParser,
        private_key: str,
        topics: List[str],
        redis_addr: str = "127.0.0.1:6379",
        fee_recipient: Optional[str] = None,
        expire_in: int = 60,
        is_testnet: bool = False,
    ):
        # self.configs = configs
        self.tob_ask_for_price = None
        self.tob_ask_against_price = None
        self.tob_bid_for_price = None
        self.tob_bid_against_price = None

        self.bid_orderbook = None
        self.ask_orderbook = None

        self.position = None
        self.last_trade = None
        self.granters: List[BinaryStateGranter] = []  # get_perp_granters(configs, [], n_markets=1)
        self.last_granter_update = 0
        self.consumer = self.get_consumer(redis_addr, topics)

        # local orders
        self.buy_for_orders = {}
        self.buy_against_orders = {}
        self.sell_for_orders = {}
        self.sell_against_orders = {}

        self.gas_price = 500000000

        nodes = ["sentry0", "sentry1", "sentry3", "k8s"]
        (
            self.node_idx,
            self.network,
            self.composer,
            self.client,
            self.lcd_endpoint,
        ) = create_client(node_idx=3, nodes=nodes, is_testnet=is_testnet)

        self.lcd_endpoint = self.network.lcd_endpoint
        # load account
        self.priv_key: PrivateKey = PrivateKey.from_hex(private_key)
        self.pub_key: PublicKey = self.priv_key.to_public_key()
        logging.info(f"self.network.lcd_endpoint: {self.lcd_endpoint}")
        self.address = self.pub_key.to_address().init_num_seq(self.lcd_endpoint)
        self.inj_address = self.address.to_acc_bech32()
        self.subaccount_id = self.address.get_subaccount_id(index=0)
        logging.debug(self.subaccount_id)

        if not fee_recipient:
            self.fee_recipient = self.inj_address
        else:
            self.fee_recipient = fee_recipient

        self.expire_in = expire_in

    async def on_tob(self, data):
        self.tob_bid_price = data[0]
        self.tob_ask_price = data[0]

    async def on_trade(self, data):
        self.last_trade = data
        logging.debug(data)

    async def on_depth(self, data):
        self.bid_orderbook = data["bid"]
        self.ask_orderbook = data["ask"]

    async def on_position(self, data):
        self.position = data

    async def on_probabilities(self, probabilities):
        """
        Probabilities object
        TODO:
            3 events market
            2 events market
        """
        raise NotImplementedError("Subclasses should implement this!")

    def get_consumer(self, redis_addr: str, topics: List[str]):
        return RedisConsumer(
            redis_addr,
            topics=topics,
            on_tob=self.on_tob,
            on_trade=self.on_trade,
            on_depth=self.on_depth,
            on_position=self.on_position,
            on_probabilities=self.on_probabilities,
        )

    async def get_granters_portfolio(self):
        raise NotImplementedError("Subclasses should implement this!")

    async def batch_replace_orders(self):
        msg = self._build_batch_replace_orders_msg()
        msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
        return await execute(
            pub_key=self.pub_key,
            priv_key=self.priv_key,
            address=self.address,
            network=self.network,
            client=self.client,
            composer=self.composer,
            gas_price=self.gas_price,
            msg=msg,
        )

    async def batch_new_orders(self, orders: List):
        msg = self._build_batch_new_orders_msg(orders=orders)
        logging.debug(f"msg: {msg}")
        msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
        return await execute(
            pub_key=self.pub_key,
            priv_key=self.priv_key,
            address=self.address,
            network=self.network,
            client=self.client,
            composer=self.composer,
            gas_price=self.gas_price,
            msg=msg,
        )

    async def batch_cancel(self, cancel_current_open_orders=False):
        if cancel_current_open_orders:
            msg = self._build_cancel_all_current_open_orders()
        else:
            msg = self._build_batch_cancel_all_orders_msg()
        msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
        return await execute(
            pub_key=self.pub_key,
            priv_key=self.priv_key,
            address=self.address,
            network=self.network,
            client=self.client,
            composer=self.composer,
            gas_price=self.gas_price,
            msg=msg,
        )

    def _build_batch_replace_orders_msg(self):
        raise NotImplementedError("Subclasses should implement this!")

    def _build_batch_new_orders_msg(self, orders: List[Order]):
        raise NotImplementedError("Subclasses should implement this!")

    def _build_batch_cancel_all_orders_msg(self):
        tmp_binary_options_market_ids_to_cancel_all = []

        for granter in self.granters:

            tmp = [limit_order.msg for limit_order in granter.limit_orders] + [
                market_order.msg for market_order in granter.market_orders
            ]
            tmp_binary_options_market_ids_to_cancel_all.extend(set(tmp))

        binary_options_market_ids_to_cancel_all = list(set(tmp_binary_options_market_ids_to_cancel_all))
        if not binary_options_market_ids_to_cancel_all:
            for granter in self.granters:
                # print(f"marekt id: {granter.market.market_id}")
                binary_options_market_ids_to_cancel_all.append(granter.market.market_id)

        logging.info(f"Canceling {binary_options_market_ids_to_cancel_all}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
        )
        return msg

    def _build_cancel_all_current_open_orders(self):
        binary_options_market_ids_to_cancel_all = []
        for granter in self.granters:
            # print(f"marekt id: {granter.market.market_id}")
            binary_options_market_ids_to_cancel_all.append(granter.market.market_id)

        logging.info(f"Canceling {binary_options_market_ids_to_cancel_all}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
        )
        return msg

    async def get_orders(self):
        raise NotImplementedError("Subclasses should implement this!")

    async def _get_orders(self, market: Market, subaccount_id: str):
        orders = await self.client.get_historical_derivative_orders(
            market_id=market.market_id,
            subaccount_id=subaccount_id,
            state="booked",  # TODO need to test if partial filled is included in booked
        )
        async for order in orders:
            if order.order_type == "buy" and not order.is_reduce_only:
                print("buy_for")
                self.buy_for_orders[order.order_hash] = order
            elif order.order_type == "sell" and not order.is_reduce_only:
                print("buy_against")
                self.buy_against_orders[order.order_hash] = order
            elif order.order_type == "buy" and order.is_reduce_only:
                print("sell_against")
                self.sell_against_orders[order.order_hash] = order
            elif order.order_type == "sell" and order.is_reduce_only:
                print("sell_for")
                self.sell_for_orders[order.order_hash] = order
            else:
                print("unknown order type")

    async def get_positions(self):
        # TODO
        raise NotImplemented("Subclasses should implement this")

    def get_loop(self):
        return get_event_loop()

    async def run(self, t=10):
        raise NotImplementedError("Subclasses should implement this!")
