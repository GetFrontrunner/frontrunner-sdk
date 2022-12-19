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

from utils.markets import multi_states_markets_factory  # , Market, ActiveMarket, StagingMarket

from utils.multi_state_market_granter import MultiStateGranter
from utils.get_markets import get_all_active_markets, get_all_staging_markets
from utils.utilities import RedisConsumer, get_nonce
from utils.objects import Order, Probability, Probabilities
from utils.markets import Market, ActiveMarket, StagingMarket, MultiStatesMarket
from chain.execution import execute
from chain.client import create_client, switch_node_recreate_client
import logging

from asyncio import sleep, get_event_loop
from dotenv import load_dotenv
from configparser import ConfigParser
from strategy.market_making import Model


load_dotenv()


class MultiStatesMarketModel(Model):
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
        self.granters: List[MultiStateGranter] = []  # get_perp_granters(configs, [], n_markets=1)
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

    # async def on_tob(self, data):
    #    self.tob_bid_price = data[0]
    #    self.tob_ask_price = data[0]

    # async def on_trade(self, data):
    #    self.last_trade = data
    #    logging.debug(data)

    # async def on_depth(self, data):
    #    self.bid_orderbook = data["bid"]
    #    self.ask_orderbook = data["ask"]

    # async def on_position(self, data):
    #    self.position = data

    async def on_probabilities(self, probabilities):
        """
        Probabilities object
            3 events market
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

    # def get_consumer(self, redis_addr: str, topics: List[str]):
    #    return RedisConsumer(
    #        redis_addr,
    #        topics=topics,
    #        on_tob=self.on_tob,
    #        on_trade=self.on_trade,
    #        on_depth=self.on_depth,
    #        on_position=self.on_position,
    #        on_probabilities=self.on_probabilities,
    #    )

    async def get_granters_portfolio(self):
        if self.granters:
            for granter in self.granters:
                portfolio = await self.client.get_portfolio(granter.inj_address)
                granter.available_balance = float(portfolio.portfolio.subaccounts[0].available_balance)
                granter.locked_balance = float(portfolio.portfolio.subaccounts[0].locked_balance)
                logging.debug(f"granter: {granter.inj_address}")
                logging.debug(f"buy market: {granter.buy_market.ticker}, market id: {granter.buy_market.market_id}")
                logging.debug(f"sell market: {granter.sell_market.ticker}, market id: {granter.sell_market.market_id}")
                logging.debug(f"draw market: {granter.draw_market.ticker}, market id: {granter.draw_market.market_id}")
                logging.debug(
                    f"available_balance: {granter.available_balance}, locked_balance: {granter.locked_balance}"
                )
                logging.debug(portfolio)

    def update_granters(self):
        # not suppored for now because Authz is broken
        pass
        # if self.configs:
        #    self.perp_granters = get_perp_granters(
        #        self.configs, self.perp_granters, n_markets=1
        #    )
        # else:
        #    raise Exception("No config")

    def _create_granter_for_multi_states_market(
        self, lcd_endpoint: str, buy_market: ActiveMarket, sell_market: ActiveMarket, draw_market: ActiveMarket
    ) -> MultiStateGranter:
        granter = MultiStateGranter(
            buy_market=buy_market,
            sell_market=sell_market,
            draw_market=draw_market,
            inj_address=self.inj_address,
            fee_recipient=self.inj_address,
        )
        granter.get_nonce(lcd_endpoint)
        logging.debug(f"granter: {granter.inj_address}, nonce: {granter.nonce}")
        logging.debug(f"buy market: {granter.buy_market.ticker}, market id: {granter.buy_market.market_id}")
        logging.debug(f"sell market: {granter.sell_market.ticker}, market id: {granter.sell_market.market_id}")
        logging.debug(f"draw market: {granter.draw_market.ticker}, market id: {granter.draw_market.market_id}")
        return granter

    def create_granters_for_multi_states_markets(self, ticker: Optional[str] = None):
        all_active_markets = get_all_active_markets(True)
        granters = []
        if ticker:
            pass
        else:
            for idx, active_markets in enumerate(all_active_markets.values()):
                if isinstance(active_markets, MultiStatesMarket):
                    # TODO only the first market works, need to fix this part
                    for active_market in active_markets:
                        granters.append(
                            self._create_granter_for_multi_states_market(
                                lcd_endpoint=self.lcd_endpoint,
                                buy_market=active_markets[0],
                                sell_market=active_markets[1],
                                draw_market=active_markets[2],
                            )
                        )

        self.granters = granters
        for granter in self.granters:
            logging.info(f"market ticker: {granter.buy_market.ticker}")
            logging.info(f"market ticker: {granter.sell_market.ticker}")
            logging.info(f"market ticker: {granter.draw_market.ticker}")

    def _create_orders_for_granters_multi_states_market(
        self, granter: MultiStateGranter, event_1: Event, event_2: Event, event_3: Event
    ) -> List[Order]:
        return [
            granter.create_order(
                price=event_1.price,
                quantity=event_1.quantity,
                is_limit=event_1.is_limit,
                is_bid=event_1.is_bid,
                is_for=event_1.is_for,
                market=granter.buy_market,
                composer=self.composer,
            ),
            granter.create_order(
                price=event_2.price,
                quantity=event_2.quantity,
                is_limit=event_2.is_limit,
                is_bid=event_2.is_bid,
                is_for=event_2.is_for,
                market=granter.sell_market,
                composer=self.composer,
            ),
            granter.create_order(
                price=event_3.price,
                quantity=event_3.quantity,
                is_limit=event_3.is_limit,
                is_bid=event_3.is_bid,
                is_for=event_3.is_for,
                market=granter.draw_market,
                composer=self.composer,
            ),
        ]

    def create_orders_for_granters(self, event_1, event_2) -> List[Order]:
        if self.granters:
            for granter in self.granters:
                event_1 = Event(price=0.32, quantity=12, is_bid=True, is_for=True, is_limit=True)
                event_2 = Event(price=0.40, quantity=1, is_bid=True, is_for=True, is_limit=True)
                event_3 = Event(price=0.10, quantity=39, is_bid=True, is_for=True, is_limit=True)
                return self._create_orders_for_granters_multi_states_market(
                    granter, event_1=event_1, event_2=event_2, event_3=event_3
                )
        raise Exception("No granter")

    # async def batch_replace_orders(self):
    #    msg = self._build_batch_replace_orders_msg()
    #    msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
    #    return await execute(
    #        pub_key=self.pub_key,
    #        priv_key=self.priv_key,
    #        address=self.address,
    #        network=self.network,
    #        client=self.client,
    #        composer=self.composer,
    #        gas_price=self.gas_price,
    #        msg=msg,
    #    )

    # async def batch_new_orders(self, orders: List[Order]):
    #    msg = self._build_batch_new_orders_msg(orders=orders)
    #    logging.debug(f"msg: {msg}")
    #    msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
    #    return await execute(
    #        pub_key=self.pub_key,
    #        priv_key=self.priv_key,
    #        address=self.address,
    #        network=self.network,
    #        client=self.client,
    #        composer=self.composer,
    #        gas_price=self.gas_price,
    #        msg=msg,
    #    )

    # async def batch_cancel(self, cancel_current_open_orders=False):
    #    if cancel_current_open_orders:
    #        msg = self._build_cancel_all_current_open_orders()
    #    else:
    #        msg = self._build_batch_cancel_all_orders_msg()
    #    msg = self.composer.MsgExec(grantee=self.inj_address, msgs=[msg])
    #    return await execute(
    #        pub_key=self.pub_key,
    #        priv_key=self.priv_key,
    #        address=self.address,
    #        network=self.network,
    #        client=self.client,
    #        composer=self.composer,
    #        gas_price=self.gas_price,
    #        msg=msg,
    #    )

    def _build_batch_replace_orders_msg(self):
        multi_options_orders_to_create = []
        multi_options_orders_to_cancel = []
        multi_options_market_ids_to_cancel_all = []

        for granter in self.granters:
            tmp = [limit_order.msg for limit_order in granter.limit_orders] + [
                market_order.msg for market_order in granter.market_orders
            ]
            multi_options_orders_to_create.extend(tmp)

        multi_options_market_ids_to_cancel_all = list(
            set([order.market.market_id for order in multi_options_orders_to_create])
        )
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_orders_to_create=multi_options_orders_to_create,
            binary_options_orders_to_cancel=multi_options_orders_to_cancel,
            binary_options_market_ids_to_cancel_all=multi_options_market_ids_to_cancel_all,
        )
        return msg

    def _build_batch_new_orders_msg(self, orders: List[Order]):
        multi_options_orders_to_create = []

        for granter in self.granters:
            tmp = [order.msg for order in orders]
            logging.debug(f"len(tmp): {len(tmp)}")
            multi_options_orders_to_create.extend(tmp)

        logging.debug(f"grantee inj address: {self.inj_address}")
        logging.debug(multi_options_orders_to_create)
        logging.info(f"n orders to create: {len(multi_options_orders_to_create)}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            binary_options_orders_to_create=multi_options_orders_to_create,
        )
        return msg

    def _build_batch_cancel_all_orders_msg(self):
        tmp_multi_options_market_ids_to_cancel_all = []

        for granter in self.granters:

            tmp = [limit_order.msg for limit_order in granter.limit_orders] + [
                market_order.msg for market_order in granter.market_orders
            ]
            tmp_multi_options_market_ids_to_cancel_all.extend(set(tmp))

        multi_options_market_ids_to_cancel_all = list(set(tmp_multi_options_market_ids_to_cancel_all))
        if not multi_options_market_ids_to_cancel_all:
            for granter in self.granters:
                # print(f"marekt id: {granter.market.market_id}")
                multi_options_market_ids_to_cancel_all.extend(
                    [granter.buy_market.market_id, granter.sell_market.market_id, granter.draw_market.market_id]
                )

        logging.info(f"Canceling {multi_options_market_ids_to_cancel_all}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=multi_options_market_ids_to_cancel_all,
        )
        return msg

    def _build_cancel_all_current_open_orders(self):
        multi_options_market_ids_to_cancel_all = []
        for granter in self.granters:
            # print(f"marekt id: {granter.market.market_id}")
            multi_options_market_ids_to_cancel_all.extend(
                [granter.buy_market.market_id, granter.sell_market.market_id, granter.draw_market.market_id]
            )

        logging.info(f"Canceling {multi_options_market_ids_to_cancel_all}")
        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.inj_address,
            subaccount_id=self.subaccount_id,
            binary_options_market_ids_to_cancel_all=multi_options_market_ids_to_cancel_all,
        )
        return msg

    async def get_orders(self):
        for granter in self.granters:

            self.buy_for_orders.clear()
            self.buy_against_orders.clear()
            self.sell_for_orders.clear()
            self.sell_against_orders.clear()
            await self._get_orders(granter.buy_market, granter.subaccount_id)
            await self._get_orders(granter.sell_market, granter.subaccount_id)
            await self._get_orders(granter.draw_market, granter.subaccount_id)

    async def _get_orders(self, market: Market, subaccount_id: str):
        orders = await self.client.get_historical_derivative_orders(
            market_id=market.market_id,
            subaccount_id=subaccount_id,
            state="booked",  # TODO need to test if partial filled is included in booked
        )
        async for order in orders:
            if order.order_type == "buy" and order.is_reduce_only == False:
                print("buy_for")
                self.buy_for_orders[order.order_hash] = order
            elif order.order_type == "sell" and order.is_reduce_only == False:
                print("buy_against")
                self.buy_against_orders[order.order_hash] = order
            elif order.order_type == "buy" and order.is_reduce_only == True:
                print("sell_against")
                self.sell_against_orders[order.order_hash] = order
            elif order.order_type == "sell" and order.is_reduce_only == True:
                print("sell_for")
                self.sell_for_orders[order.order_hash] = order
            else:
                print("unknown order type")

    def get_loop(self):
        return get_event_loop()

    async def run(self, t=10):
        logging.info("cancel all current open orders")
        resp = await self.batch_cancel(cancel_current_open_orders=True)
        logging.info(resp)
        logging.info("getting data")
        logging.info(f"sleep for {t}s")
        await sleep(t)
        logging.info(f"slept {t}s")
        self.create_granters_for_multi_states_markets()

        while True:
            await sleep(200)
            logging.info("will cancell all orders in 200s")
            # await sleep(5)
            resp = await self.batch_cancel()
            logging.info(resp)
        logging.info("finished")
