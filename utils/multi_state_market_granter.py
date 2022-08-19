from pyinjective.composer import Composer
from pyinjective.wallet import Address
from pyinjective.constant import Denom
import logging
from typing import List, Tuple, Optional

from utils.objects import (
    Order,
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


class MultiStateGranter:
    def __init__(
        self, buy_market: Market, sell_market: Market, draw_market: Market, inj_address: str, fee_recipient: str
    ):
        self.buy_market = buy_market
        self.sell_market = sell_market
        self.draw_market = draw_market

        self.limit_buy_for = LimitOrders()
        self.limit_buy_against = LimitOrders()
        self.limit_sell_for = LimitOrders()
        self.limit_sell_against = LimitOrders()
        self.limit_draw_for = LimitOrders()
        self.limit_draw_against = LimitOrders()

        self.market_buy_for = MarketOrders()
        self.market_buy_against = MarketOrders()
        self.market_sell_for = MarketOrders()
        self.market_sell_against = MarketOrders()
        self.market_draw_for = MarketOrders()
        self.market_draw_against = MarketOrders()

        self.limit_orders = []
        self.market_orders = []
        # self.buy_market_orders = MarketOrders()
        ## self.buy_market_against = MarketOrders()
        # self.sell_market_orders = MarketOrders()
        ## self.sell_market_against = MarketOrders()
        # self.draw_market_orders = MarketOrders()
        ## self.draw_market_against = MarketOrders()

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


    def create_order(
        self,
        price: float,
        quantity: int,
        is_limit: Optional[bool],
        is_bid: bool,
        is_for: bool,
        market: Market,
        composer: Composer,
    ) -> Order:

        logging.info(f"market id: {market.market_id}")
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
        return Order(
            nonce=self.nonce,
            price=price,
            quantity=quantity,
            order_type="limit" if is_limit else "market",
            subaccount_id=self.subaccount_id,
            fee_recipient=self.fee_recipient,
            inj_address=self.inj_address,
            is_buy=is_bid,
            is_for=is_for,
            market=market,
            denom=self.denom,
            composer=composer,
        )


    def _cancel_order(
        self,
        orderhash: str,
        composer: Composer,
    ):
        # TODO find the correct market to delete orders
        if self.buy_market.market_id:

            self.limit_buy_for.remove_by_orderhash(orderhash)
            self.limit_buy_against.remove_by_orderhash(orderhash)
            self.limit_sell_for.remove_by_orderhash(orderhash)
            self.limit_sell_against.remove_by_orderhash(orderhash)
            self.limit_draw_for.remove_by_orderhash(orderhash)
            self.limit_draw_against.remove_by_orderhash(orderhash)
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

        self.limit_buy_for.remove_by_orderhash(orderhash)  # = LimitOrders()
        self.limit_buy_against.remove_by_orderhash(orderhash)  # = LimitOrders()
        self.limit_sell_for.remove_by_orderhash(orderhash)  # = LimitOrders()
        self.limit_sell_against.remove_by_orderhash(orderhash)  # = LimitOrders()
        self.limit_draw_for.remove_by_orderhash(orderhash)  # = LimitOrders()
        self.limit_draw_against.remove_by_orderhash(orderhash)  # = LimitOrders()

        self.market_buy_for.remove_by_orderhash(orderhash)  # = MarketOrders()
        self.market_buy_against.remove_by_orderhash(orderhash)  # = MarketOrders()
        self.market_sell_for.remove_by_orderhash(orderhash)  # = MarketOrders()
        self.market_sell_against.remove_by_orderhash(orderhash)  # = MarketOrders()
        self.market_draw_for.remove_by_orderhash(orderhash)  # = MarketOrders()
        self.market_draw_against.remove_by_orderhash(orderhash)  # = MarketOrders()

