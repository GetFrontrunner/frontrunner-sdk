from pyinjective.composer import Composer
from pyinjective.wallet import Address
from pyinjective.constant import Denom
import logging
from typing import List, Tuple

from utils.objects import (
    LimitOrder,
    MarketOrder,
    MarketOrders,
    LimitOrders,
    LimitBuyForOrder,
    LimitBuyAgainstOrder,
    MarketBuyForOrder,
    MarketBuyAgainstOrder,
)
from utils.markets import Market
from utils.utilities import get_nonce

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)-3d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


class MultiStatesGranter:
    def __init__(
        self, buy_market: Market, sell_market: Market, draw_market: Market, inj_address: str, fee_recipient: str
    ):
        self.buy_market = buy_market
        self.sell_market = sell_market
        self.draw_market = draw_market

        self.buy_limit_orders = LimitOrders()
        # self.buy_limit_against = LimitOrders()
        self.sell_limit_orders = LimitOrders()
        # self.sell_limit_against = LimitOrders()
        self.draw_limit_orders = LimitOrders()
        # self.draw_limit_against = LimitOrders()

        self.buy_market_orders = MarketOrders()
        # self.buy_market_against = MarketOrders()
        self.sell_market_orders = MarketOrders()
        # self.sell_market_against = MarketOrders()
        self.draw_market_orders = MarketOrders()
        # self.draw_market_against = MarketOrders()

        self.fee_recipient = fee_recipient
        self.inj_address = inj_address
        self.granter_address = Address.from_acc_bech32(inj_address)
        self.subaccount_id = self.granter_address.get_subaccount_id(index=0)
        logging.debug(f"granter: inj address: {self.inj_address}, subaccount id: {self.subaccount_id}")
        self.denom = Denom(
            description="desc",
            base=0,
            quote=6,
            min_price_tick_size=1000,
            min_quantity_tick_size=0.0001,
        )
        self.available_balance: float = 0.0
        self.locked_balance: float = 0.0
        self.nonce = 0

    def get_nonce(self, lcd_endpoint: str):
        self.nonce = get_nonce(lcd_endpoint=lcd_endpoint, subaccount_id=self.subaccount_id)

    def update_nonce(self):
        self.nonce += 1

    def create_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_bid: bool,
        is_for: bool,
        state: int,
        composer: Composer,
    ):
        logging.info(f"market id: {self.buy_market.market_id}")
        self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        # logging.info(
        #    f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}"
        # )
        # Injective order params:
        # * BUY_FOR: is_buy = True is_reduce = False
        # * BUY_AGAINST: is_buy = False and is_reduce = False
        # * SELL_AGAINST: is_buy = True and is_reduce = True
        # * SELL_FOR: is_buy = False and is_reduce = True
        if state == 0:
            if is_bid:
                if is_for:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
            else:
                if is_for:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)

        if state == 1:
            if is_bid:
                if is_for:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
            else:
                if is_for:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)

        if state == 2:
            if is_bid:
                if is_for:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_bid_order(price, quantity, is_limit, is_for, composer)
            else:
                if is_for:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)
                else:
                    self._create_ask_order(price, quantity, is_limit, is_for, composer)

    def _create_bid_order(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_for: bool,
        # state:int,
        composer: Composer,
    ):
        logging.debug(f"nonce: {self.nonce}")
        logging.info(f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}")
        self.buy_limit_orders.list.clear()
        self.buy_market_orders.list.clear()
        if is_limit:
            order = LimitOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                is_for=is_for,
                market=self.buy_market,
                denom=self.denom,
                composer=composer,
            )
            self.buy_limit_orders.add(order)
        else:
            order = MarketOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                is_for=is_for,
                market=self.buy_market,
                denom=self.denom,
                composer=composer,
            )
            self.buy_market_orders.add(order)

    def _create_ask_order(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_for: bool,
        # state:int,
        composer: Composer,
    ):
        # self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        logging.debug(f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}")
        if is_limit:
            order = LimitOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.sell_market,
                denom=self.denom,
                composer=composer,
            )
            self.sell_limit_orders.add(order)
        else:
            order = MarketOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.sell_market,
                denom=self.denom,
                composer=composer,
            )
            self.sell_market_orders.add(order)

    def _create_draw_order(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_for: bool,
        # state:int,
        composer: Composer,
    ):
        # self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        logging.debug(f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}")
        if is_limit:
            order = LimitOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.draw_market,
                denom=self.denom,
                composer=composer,
            )
            self.draw_limit_orders.add(order)
        else:
            order = MarketOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.draw_market,
                denom=self.denom,
                composer=composer,
            )
            self.draw_market_orders.add(order)

    def _cancel_order(
        self,
        orderhash: str,
        composer: Composer,
    ):
        # TODO find the correct market to delete orders
        if self.buy_market.market_id:
            self.buy_limit_orders.remove_by_orderhash(orderhash)
            self.sell_limit_orders.remove_by_orderhash(orderhash)
            self.draw_limit_orders.remove_by_orderhash(orderhash)
            self.buy_market_orders.remove_by_orderhash(orderhash)
            self.sell_market_orders.remove_by_orderhash(orderhash)
            self.draw_market_orders.remove_by_orderhash(orderhash)
            return composer.MsgCancelBinaryOptionsOrder(
                sender=self.inj_address,
                market_id=self.buy_market.market_id,
                subaccount_id=self.subaccount_id,
                order_hash=orderhash,
            )
        raise Exception("Market id is missing")

    def batch_update_orders(self, price_quantity: List[Tuple[float, int]], composer: Composer):
        pass

    def pop_filled_orders(self, orderhash: str):
        self.buy_limit_orders.remove_by_orderhash(orderhash)
        self.sell_limit_orders.remove_by_orderhash(orderhash)
        self.draw_limit_orders.remove_by_orderhash(orderhash)
        self.buy_market_orders.remove_by_orderhash(orderhash)
        self.sell_market_orders.remove_by_orderhash(orderhash)
        self.draw_market_orders.remove_by_orderhash(orderhash)
        # self.market_bids.remove_by_orderhash(orderhash)
        # self.market_asks.remove_by_orderhash(orderhash)


class BiStatesGranter:
    def __init__(self, market: Market, inj_address: str, fee_recipient: str):
        self.market = market

        self.limit_buy_for = LimitOrders()
        self.limit_buy_against = LimitOrders()
        self.limit_ask_for = LimitOrders()
        self.limit_ask_against = LimitOrders()
        self.market_bid_for = MarketOrders()
        self.market_bid_against = MarketOrders()
        self.market_ask_for = MarketOrders()
        self.market_ask_against = MarketOrders()

        self.limit_asks = LimitOrders()
        self.limit_bids = LimitOrders()
        self.market_asks = MarketOrders()
        self.market_bids = MarketOrders()

        self.fee_recipient = fee_recipient
        self.inj_address = inj_address
        self.granter_address = Address.from_acc_bech32(inj_address)
        self.subaccount_id = self.granter_address.get_subaccount_id(index=0)
        logging.debug(f"granter: inj address: {self.inj_address}, subaccount id: {self.subaccount_id}")
        self.denom = Denom(
            description="desc",
            base=0,
            quote=6,
            min_price_tick_size=1000,
            min_quantity_tick_size=0.0001,
        )
        self.available_balance: float = 0.0
        self.locked_balance: float = 0.0
        self.nonce = 0

    def get_nonce(self, lcd_endpoint: str):
        self.nonce = get_nonce(lcd_endpoint=lcd_endpoint, subaccount_id=self.subaccount_id)

    def update_nonce(self):
        self.nonce += 1

    def create_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_bid: bool,
        is_for: bool,
        composer: Composer,
    ):
        logging.info(f"market id: {self.market.market_id}")
        self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        # logging.info(
        #    f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}"
        # )
        # Injective order params:
        # * BUY_FOR: is_buy = True is_reduce = False
        # * BUY_AGAINST: is_buy = False and is_reduce = False
        # * SELL_AGAINST: is_buy = True and is_reduce = True
        # * SELL_FOR: is_buy = False and is_reduce = True
        if is_bid:
            if is_for:
                self._create_bid_order(price, quantity, is_limit, is_for, composer)
            else:
                self._create_bid_order(price, quantity, is_limit, is_for, composer)
        else:
            if is_for:
                self._create_ask_order(price, quantity, is_limit, is_for, composer)
            else:
                self._create_ask_order(price, quantity, is_limit, is_for, composer)

    def _create_bid_order(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_for: bool,
        composer: Composer,
    ):
        # logging.info(f"market id: {self.market.market_id}")
        # self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        logging.info(f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}")
        self.limit_asks.list.clear()
        self.limit_bids.list.clear()
        if is_limit:
            order = LimitOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                is_for=is_for,
                market=self.market,
                denom=self.denom,
                composer=composer,
            )
            self.limit_bids.add(order)
        else:
            order = MarketOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                is_for=is_for,
                market=self.market,
                denom=self.denom,
                composer=composer,
            )
            self.market_bids.add(order)

    def _create_ask_order(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        is_for: bool,
        composer: Composer,
    ):
        # self.update_nonce()
        logging.debug(f"nonce: {self.nonce}")
        logging.debug(f"subaccount_id: {self.subaccount_id}, inj address: {self.inj_address}")
        if is_limit:
            order = LimitOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.market,
                denom=self.denom,
                composer=composer,
            )
            self.limit_asks.add(order)
        else:
            order = MarketOrder(
                nonce=self.nonce,
                price=price,
                quantity=quantity,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                is_for=is_for,
                market=self.market,
                denom=self.denom,
                composer=composer,
            )
            self.market_asks.add(order)

    def _cancel_order(
        self,
        orderhash: str,
        composer: Composer,
    ):
        if self.market.market_id:
            self.limit_bids.remove_by_orderhash(orderhash)
            self.limit_asks.remove_by_orderhash(orderhash)
            self.market_bids.remove_by_orderhash(orderhash)
            self.market_asks.remove_by_orderhash(orderhash)
            return composer.MsgCancelBinaryOptionsOrder(
                sender=self.inj_address,
                market_id=self.market.market_id,
                subaccount_id=self.subaccount_id,
                order_hash=orderhash,
            )
        raise Exception("Market id is missing")

    def batch_update_orders(self, price_quantity: List[Tuple[float, int]], composer: Composer):
        pass

    def pop_filled_orders(self, orderhash: str):
        self.limit_bids.remove_by_orderhash(orderhash)
        self.limit_asks.remove_by_orderhash(orderhash)
        # self.market_bids.remove_by_orderhash(orderhash)
        # self.market_asks.remove_by_orderhash(orderhash)
