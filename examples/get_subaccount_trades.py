import argparse
from os import environ
from argparse import Namespace
from chain.injective_client import async_injective_chain_client_factory
from utils.objects import SubaccountTradesRequest, BiStateMarketMap


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("subaccount_idx", type=int, help="subaccount index. int", default=0)
    parser.add_argument(
        "execution_type",
        type=str,
        help="execution type: market, limitFill, limitMatchRestingOrder, limitMatchNewOrder. str",
    )
    parser.add_argument("direction", type=str, help="direction of trade: buy, sell. str")
    parser.add_argument("skip", type=int, help="skip the first n items. int")
    parser.add_argument("limit", type=int, help="maximum number of items to be returned")
    args = parser.parse_args()
    return args


async def get_subaccount_trades(
    subaccount_idx: int, execution_type: str, direction: str, skip: int, limit: int
) -> None:
    inj_address = environ["INJ_ADDRESS"]
    inj_private_key = environ["INJ_PRIVATE_KEY"]
    client = async_injective_chain_client_factory(
        fee_recipient_address=inj_address, priv_key_hex=inj_private_key, subaccount_idx=subaccount_idx
    )
    subaccount_trades_request = SubaccountTradesRequest(
        client.subaccount_id, BiStateMarketMap["default"], execution_type, direction, skip, limit
    )
    trades = await client.get_subaccount_trades(subaccount_trades_request)
    print(f"\n{len(trades)} trades\n")
    for trade in trades:
        print(f"{trade}")


async def main():
    namespace = parse_cli_argments()
    await get_subaccount_trades(
        namespace.subaccount_idx, namespace.execution_type, namespace.direction, namespace.skip, namespace.limit
    )
