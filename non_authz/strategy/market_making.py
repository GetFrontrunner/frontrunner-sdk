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

from pyinjective.orderhash import build_eip712_msg, domain_separator
from sha3 import keccak_256 as sha3_keccak_256


from utils.objects import Order, OrderList
from utils.markets import factory  # , Market, ActiveMarket, StagingMarket
from utils.client import create_client, switch_node_recreate_client
from utils.granter import Granter
from utils.get_markets import get_all_active_markets, get_all_staging_markets
from utils.utilities import RedisConsumer, compute_orderhash, get_nonce
from utils.markets import Market, ActiveMarket, StagingMarket
from chain.execution import execute
from chain.utilities_old import CancelOrder, LimitOrder, MarketOrder, CancelAll
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
        self.tob_bid_price = None
        self.tob_ask_price = None
        self.bid_orderbook = None
        self.ask_orderbook = None
        self.position = None
        self.last_trade = None
        self.granters: List[Granter] = []  # get_perp_granters(configs, [], n_markets=1)
        self.last_granter_update = 0
        self.consumer = self.get_consumer(redis_addr, topics)

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

    def get_consumer(self, redis_addr: str, topics: List[str]):
        return RedisConsumer(
            redis_addr,
            topics=topics,
            on_tob=self.on_tob,
            on_trade=self.on_trade,
            on_depth=self.on_depth,
            on_position=self.on_position,
        )

    async def get_granters_portfolio(self):
        if self.granters:
            for granter in self.granters:
                portfolio = await self.client.get_portfolio(granter.inj_address)
                granter.available_balance = float(
                    portfolio.portfolio.subaccounts[0].available_balance
                )
                granter.locked_balance = float(
                    portfolio.portfolio.subaccounts[0].locked_balance
                )
                logging.debug(
                    f"granter: {granter.inj_address}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
                )
                logging.debug(
                    f"available_balance: {granter.available_balance}, locked_balance: {granter.locked_balance}"
                )
                logging.debug(portfolio)

    def update_granters(self):
        pass
        # if self.configs:
        #    self.perp_granters = get_perp_granters(
        #        self.configs, self.perp_granters, n_markets=1
        #    )
        # else:
        #    raise Exception("No config")

    def _create_granter(self, lcd_endpoint: str, market: ActiveMarket) -> Granter:
        granter = Granter(
            market=market,
            inj_address=self.inj_address,
            fee_recipient=self.inj_address,
        )
        granter.get_nonce(lcd_endpoint)
        logging.debug(
            f"granter: {granter.inj_address}, nonce: {granter.nonce}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
        )
        return granter

    def create_granters(
        self,
    ):
        all_active_markets = get_all_active_markets(True)
        granters = [
            self._create_granter(
                lcd_endpoint=self.lcd_endpoint,
                market=active_market,
            )
            for idx, active_market in enumerate(all_active_markets)
        ]
        self.granters = granters[:1]
        logging.debug(f"number of granters: {len(self.granters)}")

    def update_granter_nonce(self):
        for granter in self.granters:
            granter.get_nonce(self.lcd_endpoint)

    def _create_orders_for_granters(
        self,
        granter: Granter,
        bid_price: float,
        bid_quantity: int,
        ask_price: float,
        ask_quantity: int,
        is_limit: bool,
    ):
        granter.create_orders(
            price=bid_price,
            quantity=bid_quantity,
            is_limit=is_limit,
            is_bid=True,
            composer=self.composer,
        )
        granter.create_orders(
            price=ask_price,
            quantity=ask_quantity,
            is_limit=is_limit,
            is_bid=False,
            composer=self.composer,
        )

    def create_market_orders_for_granters(self):
        if self.granters:
            for granter in self.granters:
                bid_price = 0.51
                bid_quantity = 1
                ask_price = 0.51
                ask_quantity = 1
                self._create_orders_for_granters(
                    granter,
                    bid_price=bid_price,
                    bid_quantity=bid_quantity,
                    ask_price=ask_price,
                    ask_quantity=ask_quantity,
                    is_limit=False,
                )

    def create_limit_orders_for_granters(self):
        if self.granters:
            for granter in self.granters:
                logging.info(f"granter.market.ticker: {granter.market.ticker}")
                bid_price = 0.1
                bid_quantity = 1
                ask_price = 0.49
                ask_quantity = 1
                self._create_orders_for_granters(
                    granter,
                    bid_price=bid_price,
                    bid_quantity=bid_quantity,
                    ask_price=ask_price,
                    ask_quantity=ask_quantity,
                    is_limit=True,
                )

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

    async def batch_new_orders(self):
        msg = self._build_batch_new_orders_msg()
        logging.info(f"msg: {msg}")
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

    async def batch_cancel(self):
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
        binary_options_orders_to_create = []
        binary_options_orders_to_cancel = []
        binary_options_market_ids_to_cancel_all = []

        for granter in self.granters:
            tmp = (
                [ask_order.msg for (orderhash, ask_order) in granter.limit_asks]
                + [bid_order.msg for (orderhash, bid_order) in granter.limit_bids]
                + [ask_order.msg for (orderhash, ask_order) in granter.market_asks]
                + [bid_order.msg for (orderhash, bid_order) in granter.market_bids]
            )
            binary_options_orders_to_create.extend(tmp)

        binary_options_market_ids_to_cancel_all = list(
            set([order.market.market_id for order in binary_options_orders_to_create])
        )
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
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
                [ask_order.msg for (orderhash, ask_order) in granter.limit_asks]
                + [bid_order.msg for (orderhash, bid_order) in granter.limit_bids]
                + [ask_order.msg for (orderhash, ask_order) in granter.market_asks]
                + [bid_order.msg for (orderhash, bid_order) in granter.market_bids]
            )
            logging.debug(f"len(tmp): {len(tmp)}")
            binary_options_orders_to_create.extend(tmp)
            for orderhash, ask_order in granter.limit_asks:
                logging.info(f"{orderhash}, {ask_order.hash}")
            for orderhash, bid_order in granter.limit_bids:
                logging.info(f"{orderhash}, {bid_order.hash}")

        logging.debug(f"grantee inj address: {self.inj_address}")
        logging.debug(binary_options_orders_to_create)
        logging.info(f"n orders to create: {len(binary_options_orders_to_create)}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
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
        logging.info(f"Canceling {binary_options_market_ids_to_cancel_all}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
        )
        return msg

    async def single_new_order(
        self,
        pk: str,
        price: float,
        quantity: float,
        is_buy: bool,
        is_market: bool = False,
    ):
        _market_id = self.granters[0].market.market_id
        if is_market:
            return await MarketOrder(price, quantity, is_buy, _market_id, pk)
        return await LimitOrder(price, quantity, is_buy, _market_id, pk)

    def get_loop(self):
        return get_event_loop()

    async def run(self, t=10):
        logging.info("getting data")
        logging.info(f"sleep for {t}s")
        await sleep(t)
        logging.info(f"slept {t}s")
        self.create_granters()
        while True:
            self.update_granters()
            # self.create_limit_orders_for_granters()
            # self.create_market_orders_for_granters()
            ## resp = await self.batch_new_orders()
            # resp = await self.single_new_order(
            #    pk, price=0.3, quantity=1, is_buy=True, is_market=False
            # )
            # logging.info(resp)
            # logging.info("will cancell all orders in 5s")
            # await sleep(5)
            # resp = await self.batch_cancel()
            # logging.info(resp)
            break
        logging.info("finished")
