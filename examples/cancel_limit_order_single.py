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
from chain.injective_client import async_injective_chain_client_factory
from utils.objects import OrderCancelRequest, BiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "binary_market_id",
        help="injective chain market id",
        default=BiStateMarketMap["default"],
    )
    parser.add_argument("--orderhash", help="orderhash of existing order", required=True)
    args = parser.parse_args()
    return args


async def run_cancel_limit_order(namespace: Namespace) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)
    order_hash = "<YOUR ORDER HASH>"
    order_cancel_request = OrderCancelRequest(
        subaccount_id=client.subaccount_id, market_id=namespace.binary_market_id, order_hash=namespace.orderhash
    )
    sim_res = await client.batch_update_orders([], [order_cancel_request])
    print(f"Sim response: \n{sim_res}")


async def main():
    namespace = parse_cli_argments()
    await run_cancel_limit_order(namespace)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
