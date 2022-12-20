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
    Event,
    derivative_price_from_backend,
    spot_price_from_backend,
    spot_quantity_from_backend,
)

from utils.markets import binary_states_market_factory  # , Market, ActiveMarket, StagingMarket

from utils.binary_state_market_granter import BinaryStateGranter
from utils.get_markets import get_all_active_markets, get_all_staging_markets
from utils.utilities import RedisConsumer, get_nonce
from utils.objects import Order, Probability, Probabilities
from utils.markets import Market, ActiveMarket, StagingMarket
from chain.execution import execute
from chain.client import create_client, switch_node_recreate_client
from strategy.market_making import Model
import logging

from asyncio import sleep, get_event_loop
from dotenv import load_dotenv
from configparser import ConfigParser


load_dotenv()


class BinaryMarketModel(Model):
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
        self.granters: List[BinaryStateGranter] = []
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

    async def on_probabilities(self, probabilities):
        """
        Probabilities object
        TODO:
            3 events market
            2 events market
        """
        if probabilities.outcomes:
            event_1 = probabilities.outcomes[0]
            event_2 = probabilities.outcomes[1]
            logging.info(
                f"outcome 1: id: {event_1.id}, Prob: {round(event_1.probabilities,4)}, odds: {round(event_1.odds,4)}"
            )
            logging.info(
                f"outcome 2: id: {event_2.id}, Prob: {round(event_2.probabilities,4)}, odds: {round(event_2.odds,4)}"
            )
            # TODO fix this event_1, and event 2
            orders = self.create_orders_for_granters(event_1, event_2)
            resp = await self.batch_new_orders(orders=orders)
            logging.info(resp)

        else:
            logging.info("no events in {msg['channel'].decode('utf-8')}")

    async def get_granters_portfolio(self):
        if self.granters:
            for granter in self.granters:
                portfolio = await self.client.get_portfolio(granter.inj_address)
                granter.available_balance = float(portfolio.portfolio.subaccounts[0].available_balance)
                granter.locked_balance = float(portfolio.portfolio.subaccounts[0].locked_balance)
                logging.debug(
                    f"granter: {granter.inj_address}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
                )
                logging.debug(
                    f"available_balance: {granter.available_balance}, locked_balance: {granter.locked_balance}"
                )
                logging.debug(portfolio)

    def _create_granter_for_binary_states_market(self, lcd_endpoint: str, market: ActiveMarket) -> BinaryStateGranter:
        granter = BinaryStateGranter(
            market=market,
            inj_address=self.inj_address,
            fee_recipient=self.inj_address,
        )
        granter.get_nonce(lcd_endpoint)
        logging.debug(
            f"granter: {granter.inj_address}, nonce: {granter.nonce}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
        )
        return granter

    def create_granters_for_binary_states_markets(self, ticker: Optional[str] = None):
        all_active_markets = get_all_active_markets(True)
        granters = []
        if ticker:
            pass
        else:
            for idx, active_markets in enumerate(all_active_markets.values()):
                # TODO only the first market works, need to fix this part
                if idx == 1:
                    for active_market in active_markets:
                        granters.append(
                            self._create_granter_for_binary_states_market(
                                lcd_endpoint=self.lcd_endpoint,
                                market=active_market,
                            )
                        )

        self.granters = granters
        for granter in self.granters:
            logging.info(f"market ticker: {granter.market.ticker}")
        # logging.info(f"number of granters: {len(self.granters)}")

    def _create_orders_for_granters_binary_states_market(
        self,
        granter: BinaryStateGranter,
        event_1: Event,
        event_2: Event,
    ) -> List[Order]:
        return [
            granter.create_order(
                price=event_1.price,
                quantity=event_1.quantity,
                is_limit=event_1.is_limit,
                is_bid=event_1.is_bid,
                is_for=event_1.is_for,
                composer=self.composer,
            ),
            granter.create_order(
                price=event_2.price,
                quantity=event_2.quantity,
                is_limit=event_2.is_limit,
                is_bid=event_2.is_bid,
                is_for=event_2.is_for,
                composer=self.composer,
            ),
        ]

    def create_orders_for_granters(self, event_1, event_2) -> List[Order]:
        if self.granters:
            for granter in self.granters:
                event_1 = Event(price=0.32, quantity=12, is_bid=True, is_for=True, is_limit=True)
                event_2 = Event(price=0.40, quantity=1, is_bid=True, is_for=True, is_limit=True)
                return self._create_orders_for_granters_binary_states_market(granter, event_1=event_1, event_2=event_2)
        raise Exception("No granter")

    def _build_batch_replace_orders_msg(self):
        binary_options_orders_to_create = []
        binary_options_orders_to_cancel = []
        binary_options_market_ids_to_cancel_all = []

        for granter in self.granters:
            tmp = [limit_order.msg for limit_order in granter.limit_orders] + [
                market_order.msg for market_order in granter.market_orders
            ]
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

    def _build_batch_new_orders_msg(self, orders: List[Order]):
        binary_options_orders_to_create = []

        for granter in self.granters:
            tmp = [order.msg for order in orders]
            logging.debug(f"len(tmp): {len(tmp)}")
            binary_options_orders_to_create.extend(tmp)

        logging.debug(f"grantee inj address: {self.inj_address}")
        logging.debug(binary_options_orders_to_create)
        logging.info(f"n orders to create: {len(binary_options_orders_to_create)}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            binary_options_orders_to_create=binary_options_orders_to_create,
        )
        return msg

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
        for granter in self.granters:

            self.buy_for_orders.clear()
            self.buy_against_orders.clear()
            self.sell_for_orders.clear()
            self.sell_against_orders.clear()
            await self._get_orders(granter.market, granter.subaccount_id)

    # def get_loop(self):
    #    return get_event_loop()

    async def run(self, t=10):
        logging.info("cancel all current open orders")
        resp = await self.batch_cancel(cancel_current_open_orders=True)
        logging.info(resp)
        logging.info("getting data")
        logging.info(f"sleep for {t}s")
        await sleep(t)
        logging.info(f"slept {t}s")
        self.create_granters_for_binary_states_markets()

        while True:
            # self.update_granters()
            # self.create_limit_orders_for_granters()
            # self.create_market_orders_for_granters()
            ## resp = await self.batch_new_orders()
            # resp = await self.single_new_order(
            #    pk, price=0.3, quantity=1, is_buy=True, is_market=False
            # )
            # logging.info(resp)
            await sleep(200)
            logging.info("will cancell all orders in 200s")
            # await sleep(5)
            resp = await self.batch_cancel()
            logging.info(resp)
        logging.info("finished")
