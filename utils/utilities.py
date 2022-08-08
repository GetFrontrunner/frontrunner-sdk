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
from objects import Order


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


def compute_orderhash(order: Order, lcd_endpoint: str, subaccount_id: str):
    # get starting nonce
    nonce = get_nounce(lcd_endpoint, subaccount_id)
    logging.info("starting subaccount nonce: %d" % nonce)
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
