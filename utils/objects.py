import logging

from typing import Any
from dataclasses import dataclass

from typing import Any, Optional

from sortedcontainers import SortedList

# from math import floor
# from configparser import ConfigParser
# import importlib.resources as pkg_resources
# import pyinjective
# from pyinjective.constant import Network, Denom

#### Market specific objects


class Order:
    def __init__(self, price: float, quantity: float, order_type: str, msg):
        self.price = price
        self.quantity = quantity
        self.hash: Optional[str] = None
        self.order_type = order_type
        self.msg = msg

    def __lt__(self, obj):
        return self.price < obj.price

    def __gt__(self, obj):
        return self.price > obj.price

    def __le__(self, obj):
        return self.price <= obj.price

    def __ge__(self, obj):
        return self.price >= obj.price

    def __eq__(self, obj):
        return self.price == obj.price

    def update_orderhash(self, orderhash):
        self.hash = orderhash


class OrderList:
    def __init__(self):
        self.list: SortedList = SortedList([], key=lambda x: x.price)

    def add(self, order: Order):
        self.list.add(order)

    def remove(self, orderhash: str):
        for order in self.list:
            if order.orderhash == orderhash:
                self.list.remove(order)


@dataclass(init=True, repr=True)
class CancelOrder:
    """
    Cancel an order
    """

    market_id: str
    subaccount_id: str
    order_hash: str
    msg: Any

    def __lt__(self, obj):
        return self.market_id < obj.market_id

    def __gt__(self, obj):
        return self.market_id > obj.market_id

    def __le__(self, obj):
        return self.market_id <= obj.market_id

    def __ge__(self, obj):
        return self.market_id >= obj.market_id

    def __eq__(self, obj):
        return self.market_id == obj.market_id


# @dataclass(init=True, repr=True)
# class Order:
#    """
#    order objects,
#    """
#
#    price: float
#    quantity: float
#    timestamp: int = 0
#    msg_type: str = ""  # limit market
#    order_hash: str = ""
#    market_type: str = "derivative"
#    msg: Any = None
#
#    def __lt__(self, obj):
#        return self.price < obj.price
#
#    def __gt__(self, obj):
#        return self.price > obj.price
#
#    def __le__(self, obj):
#        return self.price <= obj.price
#
#    def __ge__(self, obj):
#        return self.price >= obj.price
#
#    def __eq__(self, obj):
#        return self.price == obj.price


@dataclass(init=True, repr=True, eq=True, order=False)
class Position:
    """
    current position info
    """

    # FIXME spot position has no position stream, how to fix
    position_direction: str = ""
    position_entry_price: float = 0.0
    position_net_quantity: float = 0.0
    position_timestamp: int = 0

    trade_direction: str = ""
    trade_entry_price: float = 0.0
    trade_net_quantity: float = 0.0
    trade_timestamp: int = 0

    margin: float = 0.0
    mark_price: float = 0.0
    liquidation_price: float = 0.0
    aggregate_reduce_only_quantity: float = 0.0
    timestamp: int = 0
    order_life: float = 0

    last_direction: str = ""
    last_quantity: float = 0.0
    last_trade_price: float = 0.0
    reduce_inventory_cap: float = 5
    need_to_reduce_inventory = False
    min_order_size: float = 1.0

    def get_entry_price(self):
        if (self.position_direction == "long") and (self.trade_direction == "buy"):
            return max(self.position_entry_price, self.trade_entry_price)
        elif (self.position_direction == "short") and (self.trade_direction == "sell"):
            return min(self.position_entry_price, self.trade_entry_price)
        else:
            if self.position_direction == "long":
                return self.position_entry_price
            if self.position_direction == "short":
                return self.position_entry_price
            else:
                logging.debug(
                    "bad position: trade direction: %s, position direction: %s"
                    % (self.trade_direction, self.position_direction)
                )
                return 0.0

    def update_position(
        self,
        direction: str,
        net_quantity: float,
        entry_price: float,
        margin: float,
        liquidation_price: float,
        mark_price: float,
        aggregate_reduce_only_quantity: float,
        timestamp: int,
    ):
        if (abs(self.position_net_quantity - net_quantity) > 0.0001) or (
            abs(self.position_entry_price - entry_price) > 0.0001
        ):
            self.timestamp = timestamp
            self.order_life = 0  ### -0.1 for every extra hour
        else:
            self.order_life = timestamp - self.timestamp

        self.position_direction = direction
        self.position_entry_price = entry_price
        self.position_net_quantity = net_quantity
        self.margin = margin
        self.mark_price = mark_price
        self.liquidation_price = liquidation_price
        self.aggregate_reduce_only_quantity = aggregate_reduce_only_quantity

    def update_trade(
        self,
        trade_price: float,
        trade_quantity,
        trade_direction: str,
    ):

        self.last_trade_price = trade_price
        self.last_quantity = trade_quantity
        self.last_direction = trade_direction

        if self.trade_direction == "":
            if trade_direction == "buy":
                self.trade_entry_price = trade_price
                self.trade_net_quantity = trade_quantity
                self.trade_direction = trade_direction

            elif trade_direction == "sell":
                self.trade_entry_price = trade_price
                self.trade_net_quantity = trade_quantity
                self.trade_direction = trade_direction

        elif trade_direction == self.trade_direction:
            tmp = self.trade_net_quantity + trade_quantity
            self.trade_entry_price = (
                self.trade_entry_price * self.trade_net_quantity
                + trade_price * trade_quantity
            ) / tmp
            self.trade_net_quantity = tmp

        elif trade_direction != self.trade_direction:
            tmp = self.trade_net_quantity - trade_quantity
            if tmp < 1e-4:
                self.trade_net_quantity = abs(tmp)
                self.trade_entry_price = trade_price
                self.trade_direction = trade_direction
            elif tmp > 1e-4:
                self.trade_entry_price = max(
                    (
                        self.trade_entry_price * self.trade_net_quantity
                        - trade_price * trade_quantity
                    )
                    / tmp,
                    0.0,  # FIXME THIS is not correct
                )
                self.trade_net_quantity = tmp
            else:
                self.reset_trade()

        else:  # direction
            self.reset_trade()
        if self.trade_net_quantity / self.min_order_size >= self.reduce_inventory_cap:
            self.need_to_reduce_inventory = True
        else:
            self.need_to_reduce_inventory = False
        logging.info(
            f"need to reduce inventory: {self.need_to_reduce_inventory}, trade_net_quantity: {self.trade_net_quantity}"
        )

    def reset_position(self):
        self.position_direction = ""
        self.position_entry_price = 0.0
        self.position_net_quantity = 0.0
        self.margin = 0.0
        self.mark_price = 0.0
        self.liquidation_price = 0.0
        self.aggregate_reduce_only_quantity = 0.0
        self.timestamp = 0
        self.order_life = 0.0

    def reset_trade(self):
        self.trade_direction = ""
        self.trade_entry_price = 0.0
        self.trade_net_quantity = 0.0

    def set_position_and_trade_equal(self):
        self.trade_entry_price = self.position_entry_price
        self.trade_net_quantity = self.position_net_quantity
        if self.position_direction == "long":
            self.trade_direction = "buy"
        elif self.position_direction == "short":
            self.trade_direction = "sell"
        else:
            self.trade_direction = ""

        if self.trade_net_quantity / self.min_order_size >= self.reduce_inventory_cap:
            self.need_to_reduce_inventory = True
        else:
            self.need_to_reduce_inventory = False
        logging.info(
            f"need to reduce inventory: {self.need_to_reduce_inventory}, trade_net_quantity: {self.trade_net_quantity}"
        )

    def set_trade_and_position_equal(self):
        self.position_entry_price = self.trade_entry_price
        self.position_net_quantity = self.trade_net_quantity
        if self.trade_direction == "buy":
            self.position_direction = "long"
        elif self.trade_direction == "sell":
            self.position_direction = "short"
        else:
            self.position_direction = ""


@dataclass(init=True, repr=True, eq=True, order=False)
class Gamma:
    """
    risk preferences
    """

    lb: float = 0.1
    ub: float = 3.0
    gamma: float = 0.7
    leverage: float = 1.0

    def update(self, delta: float):
        if self.gamma < self.ub or self.gamma > self.lb:
            self.gamma += delta
            logging.info(f"current gamma: {self.gamma}")
        else:
            logging.debug("Gamma is at the boundary")


@dataclass(init=True, repr=True, eq=True, order=False)
class Spread:
    """
    bid-ask spread configs
    """

    lb: float = 10
    ub: float = 200
    spread: float = 50
    base_spread: float = 50

    def update(self, delta: float):
        if (self.lb < self.base_spread) and (self.base_spread < self.ub):
            self.base_spread += delta
            logging.info(f"current spread: {self.base_spread}")
        else:
            logging.debug(f"Spread is at the boundary {self.base_spread}")

    def get_spread(self):
        return max(self.base_spread, self.spread)

    def get_base_spread(self):
        return self.base_spread


@dataclass(init=True, repr=True, eq=True, order=False)
class Balance:
    """
    balance info
    all markets share the balance in subaccount 0
    """

    # TODO add balance control
    current_base_balance: float = 0.0
    current_quote_balance: float = 0.0
    initial_base_balance: float = 0.0
    initial_quote_balance: float = 0.0

    def update_base(self, base_balance):
        self.current_base_balance = base_balance

    def update_quote(self, quote_balance):
        self.current_quote_balance = quote_balance

    def reset_initial_balance(self):
        self.current_base_balance = self.initial_base_balance
        self.current_quote_balance = self.initial_quote_balance

    def delta(self):
        return (
            self.current_base_balance - self.initial_base_balance,
            self.current_quote_balance - self.initial_quote_balance,
        )


@dataclass(init=True, repr=True)
class DenomBalance:
    """
    denom balance
    """

    peggy: str
    # balance: Balance = Balance()

    available_balance: float = 0.0
    total_balance: float = 0.0

    initial_available_balance: float = 0.0
    initial_total_balance: float = 0.0
    net_quantity = 0.0

    def update(self, available_balance, total_balance):
        self.available_balance = available_balance
        self.total_balance = total_balance
        # self.net_quantity = self.initial_available_balance

    def update_margin(self, margin):
        self.total_balance += margin

    def update_initial_balance(self, initial_available_balance, initial_total_balance):
        self.initial_available_balance = initial_available_balance
        self.initial_total_balance = initial_total_balance
        self.available_balance = initial_available_balance
        self.total_balance = initial_total_balance

    def update_trade(self, trade_price, trade_quantity, trade_direction, is_base=True):
        if is_base:
            if trade_direction == "buy":
                self.available_balance += trade_price * trade_quantity
                self.total_balance += trade_price * trade_quantity
            else:
                self.available_balance -= trade_price * trade_quantity
                self.total_balance -= trade_price * trade_quantity
        else:
            # quote balance
            if trade_direction == "buy":
                self.available_balance -= trade_price * trade_quantity
                self.total_balance -= trade_price * trade_quantity
            else:
                self.available_balance += trade_price * trade_quantity
                self.total_balance += trade_price * trade_quantity

    def reset_balance(self):
        self.available_balance = 0.0
        self.total_balance = 0.0

    def delta_total(self):
        return self.initial_total_balance - self.total_balance

    def delta_available(self):
        return self.initial_available_balance - self.available_balance
