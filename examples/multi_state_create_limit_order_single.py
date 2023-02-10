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
    arsenal = environ["ARSENAL"]
    chelsea = environ["CHELSEA"]
    draw = environ["DRAW"]
    if not draw and not arsenal and not chelsea:
        print("can't find market id")
        return
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)

    order_create_request_arsenal = OrderCreateRequest(
        client.subaccount_id,
        market_id=arsenal,
        price=0.2,
        quantity=20,
        is_buy=True,
        is_po=True,
        is_reduce_only=False,
    )

    sim_res = await client.batch_update_orders([order_create_request_arsenal], [])
    print(f"sim response: \n{sim_res}")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
