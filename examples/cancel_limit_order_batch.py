import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from async_injective_client import async_injective_chain_client_factory
from .utils.objects import OrderCancelRequest, BiStateMarketMap


async def run() -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)
    order_hash_1 = "<YOUR ORDER HASH 1>"
    order_hash_2 = "<YOUR ORDER HASH 2>"
    order_cancel_request_1 = OrderCancelRequest(
        subaccount_id=client.subaccount_id, market_id=BiStateMarketMap["default"], order_hash=order_hash_1
    )
    order_cancel_request_2 = OrderCancelRequest(
        subaccount_id=client.subaccount_id, market_id=BiStateMarketMap["default"], order_hash=order_hash_2
    )
    sim_res = await client.batch_update_orders([], [order_cancel_request_1, order_cancel_request_2])
    print(f"sim response: \n{sim_res}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
