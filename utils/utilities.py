import os
import sys
import signal
import logging
from math import floor
from typing import Any
from dataclasses import dataclass
from configparser import ConfigParser
from typing import List, Dict, Any

import importlib.resources as pkg_resources
import pyinjective
from pyinjective.constant import Network, Denom
from asyncio import (
    create_task,
    all_tasks,
    current_task,
    gather,
    sleep,
    Task,
    CancelledError,
)
from redis import StrictRedis
from redis import asyncio as aredis
import asyncio

from requests import get
from pyinjective.orderhash import build_eip712_msg, domain_separator
from sha3 import keccak_256 as sha3_keccak_256
from orders import Order


def add_message_type(data: Dict[str, Any], msg_type):
    data["msg_type"] = msg_type
    return data


async def empty_coro(*args, **kwargs) -> None:
    pass


class RedisProducer:
    __slots__ = ("redis_producer",)

    def __init__(self, redis_addr):
        ip, port = redis_addr.split(":")
        port = int(port)
        self.redis_producer = StrictRedis(ip, port)

    def produce(self, channel: str, payload):
        #  print(channel, payload)
        self.redis_producer.publish(channel, payload)


class RedisConsumer:
    __slots__ = [
        "redis_consumer",
        "topics",
        "on_tob_callback",
        "on_trade_callback",
        "on_depth_callback",
        "on_position_callback",
    ]

    def __init__(
        self,
        redis_addr: str,
        topics: List[str],
        on_tob,
        on_trade,
        on_depth,
        on_position,
    ):
        ip, port = redis_addr.split(":")
        port = int(port)
        self.redis_consumer = aredis.from_url(
            f"redis://{ip}:{port}"
        ).pubsub()  # , health_check_interval=30, retry_on_timeout=True #socket_keepalive=True, retry=True
        self.topics = set(topics)
        self.on_position_callback = on_position
        self.on_tob_callback = on_tob
        self.on_depth_callback = on_depth
        self.on_trade_callback = on_trade

        loop = asyncio.get_event_loop()
        loop.create_task(self.aconsume())

    async def aconsume(self):
        print(f"RedisConsumer reading self.topics={self.topics}")
        if self.topics:
            await self.redis_consumer.subscribe(*self.topics)
        else:
            raise Exception("No topics to subscribe to")
        async for msg in self.redis_consumer.listen():
            try:
                print(msg)
                payload = msg

                if "tob" in payload["msg_type"]:
                    await self.on_tob_callback(payload)
                elif "depth" in payload["msg_type"]:
                    await self.on_depth_callback(payload)
                elif "trade" in payload["msg_type"]:
                    await self.on_trade_callback(payload)
                elif "position" in payload["msg_type"]:
                    await self.on_position_callback(payload)
                else:
                    print("unknown data", payload)
            except Exception as e:
                pass

    async def subscribe(self, topics):
        newsub = set(topics) - self.topics
        #  print(f"before {self.topics=}")
        #  print(f"subscribe {topics=}")
        #  print(f"subscribe {newsub=}")
        if newsub:
            await self.redis_consumer.subscribe(*newsub)
            self.topics = self.topics.union(newsub)
        #  print(f"union {self.topics=}")


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def price_cross_check(side: str, base_price: float, price: float):
    """
    check price is cross base_price
    """
    if side == "buy":
        if price >= base_price:
            return False
        return True
    elif side == "sell":
        if price <= base_price:
            return False
        return True


def round_price(price: float, price_precision: int) -> float:
    return round(price, price_precision)


def round_down_quantity(x: float, decimals: int = 4) -> float:
    return floor(x * 10**decimals) / 10.0**decimals


def near_zero(x: float) -> bool:
    return abs(x) <= 1e-6


def not_near_zero(x: float) -> bool:
    return abs(x) > 1e-6


# class Cancel:
#    def __init__(self):
#        self.orders = []
#
#
# class Profit:
#    def __init__(self):
#        self.orders = []
#        # self.time = time_ns()
#
#
# class Replace:
#    def __init__(self):
#        pass


#### Market specific objects
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


#### MultiMarkets specific objects
class MarketConfig:
    """
    market infos
    """

    def __init__(
        self, base_ticker: str, quote_ticker: str, market_type: str, node: str = "k8s"
    ):
        self.base_ticker = base_ticker
        self.quote_ticker = quote_ticker
        self.market_type = market_type.title()
        self.ini_config_dir = pkg_resources.read_text(pyinjective, "denoms_mainnet.ini")
        # read denoms configs
        self.config = ConfigParser()
        self.config.read_string(self.ini_config_dir)

        self.network = Network.mainnet(node=node)

        if market_type == "spot":
            self.base_peggy, self.base_decimals = Denom.load_peggy_denom(
                self.network.env,
                f"W{base_ticker.upper()}"
                if self.base_ticker in ["btc", "eth"]
                else self.base_ticker.upper(),
            )
        self.quote_peggy, self.quote_decimals = Denom.load_peggy_denom(
            self.network.env, quote_ticker.upper()
        )
        for section in self.config.sections():
            if len(section) == 66:
                if (
                    f"{base_ticker.upper()}/{quote_ticker.upper()}"
                    in self.config.get(section, "description")
                ) and (self.market_type in self.config.get(section, "description")):
                    self.market_id = section

        self.market_denom = Denom.load_market(self.network.env, self.market_id)


async def shutdown(loop, signal=None, config_dir: str = "./config_new.ini", job=None):
    if signal:
        logging.info(f"Received exit signal {signal.name}...")
    tasks = [task for task in all_tasks() if task is not current_task()]

    for task in tasks:
        task.cancel()

    logging.info(f"Cancelling {len(tasks)} outstanding tasks")
    res = await gather(*tasks, return_exceptions=True)
    logging.info(f"Cancelling {len(tasks)} outstanding tasks {res}")

    await sleep(5)
    config = ConfigParser()
    config.read(config_dir)
    node = config["DERIVATIVE_PARAMETERS"].get("node")

    #'sentry0',  # us, prod
    #'sentry1',  # us, prod
    #'sentry3',  # tokyo, prod,
    #'sentry.cd' # dedicated github-runner

    if node == "sentry0":
        node = "sentry1"
    elif node == "sentry1":
        node = "sentry3"
    elif node == "sentry3":
        node = "k8s"
    else:
        node = "sentry0"
    config.set("DERIVATIVE_PARAMETERS", "node", node)

    # if job:
    #   cancel_all_orders_on_exit = config["PARAMETERS"].getboolean(
    #       "cancel_all_orders_on_exit", False
    #   )
    #   logging.info(f"cancel by market id")
    #   if cancel_all_orders_on_exit:
    #       await sleep(10)
    #       logging.info(f"Cancelling all outstanding orders")
    #       cancel_all_orders = create_task(job, name="cancel_all_orders")
    #       await cancel_all_orders
    #       logging.info(f"Cancelled all outstanding orders")
    #   else:
    #       pass
    loop.stop()
    logging.info("Shutdown complete.")


def handle_exception(loop, context):
    """
    asyncio exception handler
    """
    logging.error(f"context: {context}")
    # context["message"] will always be there; but context["exception"] may not
    msg = context.get("exception", context["message"])
    logging.error(f"Caught exception: {msg}")
    logging.info("Shutting down...")
    create_task(shutdown(loop, signal=signal.SIGINT))


def handle_task_result(task: Task) -> None:
    """
    asyncio task result handler
    """

    try:
        task.result()
    except CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:  # pylint: disable=broad-except
        logging.exception("Exception raised by task = %r", task)
        raise Exception("Exception raised by task = %r", task)

    # only support msgs from single subaccount


def get_nounce(lcd_endpoint: str, subaccount_id: str) -> int:
    url = f"{lcd_endpoint}/injective/exchange/v1beta1/exchange/{subaccount_id}"
    n = 3
    while n > 0:
        res = get(url=url)
        if res.status_code != 200:
            n -= 1
            # raise Exception(f"failed to get subaccount nonce {res}")
        return res.json()["nonce"]
    return 0


def compute_order_hash(order: Order, lcd_endpoint: str, subaccount_id: str):
    # get starting nonce
    nonce = get_nounce(lcd_endpoint, subaccount_id)
    logging.info("starting subaccount nonce: %d" % nonce)
    # compute hashes
    # order_hashes = []
    # increase nonce for next order
    nonce += 1
    # construct eip712 msg
    msg = build_eip712_msg(order.msg, nonce)
    # compute order hash
    if msg is not None:
        typed_data_hash = msg.hash_struct()
        typed_bytes = b"\x19\x01" + domain_separator + typed_data_hash
        keccak256 = sha3_keccak_256()
        keccak256.update(typed_bytes)
        order_hash = keccak256.hexdigest()
        order.hash = f"0x{order_hash}"
