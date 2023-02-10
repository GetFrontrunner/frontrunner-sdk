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
from .utils.objects import OrderCreateRequest


async def run() -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    binary_market_id = environ["BINARY_MARKET"]
    if not binary_market_id:
        print("can't find market id")
        return
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)
    order_create_request = OrderCreateRequest(
        client.subaccount_id,
        market_id=binary_market_id,
        price=0.3,
        quantity=20,
        is_buy=True,
        is_po=True,
        is_reduce_only=False,
    )

    sim_res = await client.batch_update_orders([order_create_request], [])
    print(f"sim response: \n{sim_res}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
