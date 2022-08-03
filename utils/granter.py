from pyinjective.composer import Composer
from pyinjective.wallet import Address
import logging
from typing import List, Tuple

# from asyncio import create_task
# from requests import get

from objects import OrderList, Order
from markets import Market  # , ActiveMarket, StagingMarket
from utilities import compute_order_hash

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

    def create_bid_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        composer: Composer,
        lcd_endpoint: str,
    ):
        if is_limit:
            order = Order(
                price,
                quantity,
                "limit",
                self._create_limit_order(
                    price=price,
                    quantity=quantity,
                    is_buy=True,
                    composer=composer,
                ),
            )
            compute_order_hash(order, lcd_endpoint, order.msg.subaccount_id)
            self.limit_bids.add(order)
        else:
            order = Order(
                price,
                quantity,
                "market",
                self._create_market_order(
                    price=price,
                    quantity=quantity,
                    is_buy=True,
                    composer=composer,
                ),
            )
            compute_order_hash(order, lcd_endpoint, order.msg.subaccount_id)
            self.market_bids.add(order)

    def create_ask_orders(
        self,
        price: float,
        quantity: int,
        is_limit: bool,
        composer: Composer,
        lcd_endpoint: str,
    ):
        if is_limit:
            order = Order(
                price,
                quantity,
                "limit",
                self._create_limit_order(
                    price=price,
                    quantity=quantity,
                    is_buy=False,
                    composer=composer,
                ),
            )
            compute_order_hash(order, lcd_endpoint, order.msg.subaccount_id)
            self.limit_asks.add(order)
        else:
            order = Order(
                price,
                quantity,
                "market",
                self._create_market_order(
                    price=price,
                    quantity=quantity,
                    is_buy=False,
                    composer=composer,
                ),
            )
            compute_order_hash(order, lcd_endpoint, order.msg.subaccount_id)
            self.market_asks.add(order)

    def _create_limit_order(
        self,
        price: float,
        quantity: int,
        is_buy: bool,
        composer: Composer,
    ):
        if self.market.market_id:
            return composer.MsgCreateBinaryOptionsLimitOrder(
                sender=self.inj_address,
                market_id=self.market.market_id,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                price=price,
                quantity=quantity,
                is_buy=is_buy,
            )
        raise Exception("Market id is missing")

    def _create_market_order(
        self,
        price: float,
        quantity: int,
        is_buy: bool,
        composer: Composer,
    ):
        if self.market.market_id:
            return composer.MsgCreateBinaryOptionsMarketOrder(
                sender=self.inj_address,
                market_id=self.market.market_id,
                subaccount_id=self.subaccount_id,
                fee_recipient=self.fee_recipient,
                price=price,
                quantity=quantity,
                is_buy=is_buy,
            )
        raise Exception("Market id is missing")

    def _cancel_order(
        self,
        orderhash: str,
        composer: Composer,
    ):
        if self.market.market_id:
            self.limit_bids.remove(orderhash)
            self.limit_asks.remove(orderhash)
            self.market_bids.remove(orderhash)
            self.market_asks.remove(orderhash)
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
