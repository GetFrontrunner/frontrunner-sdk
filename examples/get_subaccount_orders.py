import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from chain.injective_client import async_injective_chain_client_factory
from utils.objects import SubaccountOrdersRequest, BinarySideMap, BiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("subaccount_idx", type=int, help="subaccount index, int", default=0)
    args = parser.parse_args()
    return args


async def get_subaccount_orders(subaccount_idx: int) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(
        fee_recipient_address=inj_address, priv_key_hex=inj_private_key, subaccount_idx=subaccount_idx
    )
    subaccount_orders_request = SubaccountOrdersRequest(client.subaccount_id, BiStateMarketMap["default"])
    await client.get_subaccount_orders(subaccount_orders_request)
    print(f"\n{len(client.orders)} open orders\n")
    for order in client.orders:
        print(f"{order}")


async def main():
    namespace = parse_cli_argments()
    await get_subaccount_orders(namespace.subaccount_idx)
