from pyinjective.composer import Composer
from pyinjective.wallet import Address
from pyinjective.constant import Denom
import logging
from typing import List, Tuple

from objects import OrderList, Order
from markets import Market  # , ActiveMarket, StagingMarket

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s,%(msecs)-3d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)


class Granter:
    def __init__(self, market: Market, inj_address: str, fee_recipient: str):
        self.market = market
        self.limit_bids = OrderList()
        self.limit_asks = OrderList()
        self.market_bids = OrderList()
        self.market_asks = OrderList()
        self.fee_recipient = fee_recipient
        self.inj_address = inj_address
        self.granter_address = Address.from_acc_bech32(self.inj_address)
        self.subaccount_id = self.granter_address.get_subaccount_id(index=0)
        self.denom = Denom(
            description="desc",
            base=0,
            quote=6,
            min_price_tick_size=1000,
            min_quantity_tick_size=0.0001,
        )

    def create_bid_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        market: Market,
        composer: Composer,
        lcd_endpoint: str,
    ):
        if is_limit:
            order = Order(
                price=price,
                quantity=quantity,
                order_type="limit",
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                market=market,
                denom=self.denom,
                composer=composer,
            )
            order.update_orderhash(lcd_endpoint)
            self.limit_bids.add(order)
        else:
            order = Order(
                price=price,
                quantity=quantity,
                order_type="market",
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=True,
                market=market,
                denom=self.denom,
                composer=composer,
            )
            order.update_orderhash(lcd_endpoint)
            self.market_bids.add(order)

    def create_ask_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        market: Market,
        composer: Composer,
        lcd_endpoint: str,
    ):
        if is_limit:
            order = Order(
                price=price,
                quantity=quantity,
                order_type="limit",
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                market=market,
                denom=self.denom,
                composer=composer,
            )
            order.update_orderhash(lcd_endpoint)
            self.limit_bids.add(order)
        else:
            order = Order(
                price=price,
                quantity=quantity,
                order_type="market",
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                inj_address=self.inj_address,
                is_buy=False,
                market=market,
                denom=self.denom,
                composer=composer,
            )
            order.update_orderhash(lcd_endpoint)
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

    def batch_update_orders(
        self, price_quantity: List[Tuple[float, int]], composer: Composer
    ):
        pass

    def pop_filled_orders(self, orderhash: str):
        self.limit_bids.remove_by_orderhash(orderhash)
        self.limit_asks.remove_by_orderhash(orderhash)
        # self.market_bids.remove_by_orderhash(orderhash)
        # self.market_asks.remove_by_orderhash(orderhash)
