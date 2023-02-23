import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from async_injective_client import async_injective_chain_client_factory
from .utils.objects import OrderCancelRequest, MutiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", nargs="*", help="injective chain market id", default=[MutiStateMarketMap["draw"]])
    parser.add_argument("--orderhash", nargs="*", help="orderhash of existing order", required=True)
    args = parser.parse_args()

    if len(args.state) == len(args.orderhash):
        return args
    else:
        raise Exception("args length are not same")
    return args


async def run_cancel_limit_order_batch(namespace: Namespace) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)
    order_hash_1 = "<YOUR ORDER HASH 1>"
    order_hash_2 = "<YOUR ORDER HASH 2>"
    orders_to_cancel = [
        OrderCancelRequest(
            subaccount_id=client.subaccount_id,
            market_id=MutiStateMarketMap[namespace.state[i]],
            order_hash=namespace.orderhash[i],
        )
        for i in range(len(namespace.state))
    ]
    sim_res = await client.batch_update_orders(orders_to_create=[], orders_to_cancel=orders_to_cancel)
    print(f"Sim response:\n{sim_res}")


async def main():
    namespace = parse_cli_argments()
    await run_cancel_limit_order_batch(namespace)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
