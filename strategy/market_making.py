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
from utils.markets import Market, ActiveMarket, StagingMarket, factory


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
        self.address = self.pub_key.to_address().init_num_seq(self.network.lcd_endpoint)
        self.inj_address = self.address.to_acc_bech32()
        self.subaccount_id = self.address.get_subaccount_id(index=0)

        if fee_recipient:
            self.fee_recipient = self.inj_address
        else:
            self.fee_recipient = fee_recipient

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
                print(
                    f"granter: {granter.inj_address}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
                )
                print(
                    f"available_balance: {granter.available_balance}, locked_balance: {granter.locked_balance}"
                )
                print(portfolio)
                print()

    def update_granters(self):
        pass
        # if self.configs:
        #    self.perp_granters = get_perp_granters(
        #        self.configs, self.perp_granters, n_markets=1
        #    )
        # else:
        #    raise Exception("No config")

    def create_granter(
        self, inj_address: str, lcd_endpoint: str, market: ActiveMarket
    ) -> Granter:
        # for active_market in markets:
        # if active_market.ticker == market_ticker:
        granter = Granter(
            market=market,
            inj_address=inj_address,
            fee_recipient=self.inj_address,
        )
        granter.get_nonce(lcd_endpoint)
        print(
            f"granter: {granter.inj_address}, nonce: {granter.nonce}, market: {granter.market.ticker}, market id: {granter.market.market_id}"
        )
        return granter

    def create_granters(
        self,
        inj_addresses: List[str],
    ):
        all_active_markets = get_all_active_markets(True)
        n = len(inj_addresses)
        if len(inj_addresses) < len(all_active_markets):
            granters = [
                self.create_granter(
                    inj_addresses[idx % n],
                    lcd_endpoint=self.lcd_endpoint,
                    market=active_market,
                )
                for idx, active_market in enumerate(all_active_markets)
            ]
            self.granters = granters
        print(f"number of granters: {len(self.granters)}")

    def _create_orders_for_granters(
        self,
        granter: Granter,
        bid_price: float,
        bid_quantity: int,
        ask_price: float,
        ask_quantity: int,
        is_limit: bool,
    ):
        granter.create_bid_orders(
            price=bid_price,
            quantity=bid_quantity,
            is_limit=is_limit,
            composer=self.composer,
        )
        granter.create_ask_orders(
            price=ask_price,
            quantity=ask_quantity,
            is_limit=is_limit,
            composer=self.composer,
        )

    def create_market_orders_for_granters(self):
        if self.granters:
            for granter in self.granters:
                bid_price = 0.49
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
                bid_price = 0.49
                bid_quantity = 1
                ask_price = 0.51
                ask_quantity = 1
                self._create_orders_for_granters(
                    granter,
                    bid_price=bid_price,
                    bid_quantity=bid_quantity,
                    ask_price=ask_price,
                    ask_quantity=ask_quantity,
                    is_limit=True,
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
            self.create_limit_orders_for_granters()
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


# if __name__ == "__main__":
#    # from utils.get_markets import get_all_active_markets
#
#    active_markets = get_all_active_markets(disable_error_msg=True)
#    active_market = active_markets[0]
#    print(f"market_id: {active_market.market_id}")
#
#    # Getting non-existent keys
#    grantee_private_key = os.getenv("grantee_private_key")  # None
#    grantee_inj_address = os.getenv("grantee_inj_address")  # None
#
#    granter_private_key = os.getenv("granter_private_key")  # None
#    granter_inj_address = os.getenv("granter_inj_address")  # None
#
#    if grantee_private_key and granter_inj_address:
#        model = Model(private_key=grantee_private_key, topics=[], is_testnet=True)
#        model.create_granters([granter_inj_address])
#        # model.create_granters(inj_address=[granter_inj_address])
#
#        # print(model.granters)
