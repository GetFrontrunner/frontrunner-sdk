import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from chain.injective_client import async_injective_chain_client_factory
from utils.objects import OrderCreateRequest, MutiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "state",
        help="final state in arsenal vs. chelsea game, allowed values: arsenal, chelsea, draw",
        default=MutiStateMarketMap["draw"],
    )
    parser.add_argument("price", type=float, help="order price, float", default=0.2)
    parser.add_argument("quantity", type=int, help="order quantity, int", default=20)
    # parser.add_argument("post_only", type=bool, help="post only order, bool", default=True)
    parser.add_argument("reduce_only", type=bool, help="reduce only order, bool", default=False)
    args = parser.parse_args()

    length = len(args.binary_market_id)
    if all(len(arg) == length for arg in args._dict__.values()):
        return args
    else:
        raise Exception("args length are not same")


async def run_create_limit_order_single(state: str, price: float, quantity: int, is_reduce_only: bool) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(fee_recipient_address=inj_address, priv_key_hex=inj_private_key)

    order_create_request_arsenal = OrderCreateRequest(
        client.subaccount_id,
        market_id=MutiStateMarketMap[state],
        price=price,
        quantity=quantity,
        is_buy=True,
        is_reduce_only=is_reduce_only,
    )

    sim_res = await client.batch_update_orders(orders_to_create=[order_create_request_arsenal], orders_to_cancel=[])
    print(f"sim response: \n{sim_res}")


async def main():
    namespace = parse_cli_argments()
    await run_create_limit_order_single(
        namespace.state,
        namespace.price,
        namespace.quantity,
        namespace.reduce_only,
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
