# Create a limit order using batch order functionality in a Frontrunner market.
# Prerequisite: export shell environment variables for funded wallet
# python examples/create_limit_order_single.py
# This should log the market information, order information, and orderbook before and after the order is created
"""
    1. get priv_key from env
    2. get market name from CLI, 
    3. parse market name and order side to market id (1 binary market vs 3 binary markets)
    4. send order (resend order if fails)
    5. print orderhash
"""

import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from async_injective_client import async_injective_chain_client_factory
from .utils.objects import OrderCreateRequest, BinarySideMap, BiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--binary_market_id",
        nargs="*",
        help="injective chain market id",
        default=BiStateMarketMap["default"],
    )
    parser.add_argument("--side", nargs="*", help="order side: buy or sell", default="buy")
    parser.add_argument("--price", nargs="*", type=float, help="order price, float", default=0.2)
    parser.add_argument("--quantity", nargs="*", type=int, help="order quantity, int", default=20)
    parser.add_argument("--post_only", nargs="*", type=bool, help="post only order, bool", default=True)
    parser.add_argument("--reduce_only", nargs="*", type=bool, help="reduce only order, bool", default=False)
    args = parser.parse_args()

    length = len(args.binary_market_id)
    if all(len(arg) == length for arg in args._dict__.values()):
        return args
    else:
        raise Exception("args length are not same")


async def run_create_limit_orders(namespace: Namespace) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)

    order_create_requests = [
        OrderCreateRequest(
            subaccount_id=client.subaccount_id,
            market_id=namespace.binary_market_id[i],
            price=namespace.price[i],
            quantity=namespace.quantity[i],
            is_buy=BinarySideMap[namespace.side[i]],
            is_po=namespace.post_only[i],
            is_reduce_only=namespace.reduce_only[i],
        )
        for i in range(len(namespace.binary_market_id))
    ]

    sim_res = await client.batch_update_orders(orders_to_create=order_create_requests, orders_to_cancel=[])
    print(f"sim response: \n{sim_res}")


async def main():
    namespace = parse_cli_argments()
    await run_create_limit_orders(namespace)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
