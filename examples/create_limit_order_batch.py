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

from pyinjective.composer import Composer
from pyinjective.async_client import AsyncClient
from pyinjective.transaction import Transaction
from pyinjective.constant import Network
from pyinjective.wallet import PrivateKey, Address


async def run(
    market_name_one, order_side_one, price_one, quantity_one, market_name_two, order_side_two, price_two, quantity_two
) -> None:
    # select network: local, testnet, mainnet
    network = Network.testnet()
    composer = Composer(network=network.string())

    # initialize grpc client
    client = AsyncClient(network, insecure=False)
    await client.sync_timeout_height()

    # load account
    priv_key = PrivateKey.from_hex(get_env_variable("INJ_PRIVATE_KEY"))
    pub_key = priv_key.to_public_key()
    address = await pub_key.to_address().async_init_num_seq(network.lcd_endpoint)
    subaccount_id = address.get_subaccount_id(index=0)

    # prepare trade info
    fee_recipient = get_env_variable("INJ_ADDRESS")

    msg = build_msg(
        composer,
        address,
        subaccount_id,
        market_name_one,
        order_side_one,
        price_one,
        quantity_one,
        market_name_two,
        order_side_two,
        price_two,
        quantity_two,
    )
    tx = build_tx(msg, address, network)

    retry_attempt = 0
    while retry_attempt < 3:
        sim_res = await simulate_and_send_tx(client, composer, network, address, pub_key, tx, retry_attempt)
        if sim_res:
            print(f"simulate error {sim_res}")
            if "account sequence mismatch" in sim_res.details():
                address = init_num_sequence(address, network, pub_key)
            else:
                print("unhandled simulation error")
        if retry_attempt <= 3 and not sim_res:
            print("succeeded")
            return
        retry_attempt += 1
    print("failed to send order")


def build_msg(
    composer: Composer,
    address: Address,
    subaccount_id: str,
    market_name_one: str,
    order_side_one: str,
    price_one: float,
    quantity_one: int,
    market_name_two: str,
    order_side_two: str,
    price_two: float,
    quantity_two: int,
):

    # build msg
    binary_options_market_one_id_create = get_market_id(market_name_one, order_side_one)
    binary_options_market_one_id_cancel = binary_options_market_one_id_create

    binary_options_market_two_id_create = get_market_id(market_name_two, order_side_two)
    binary_options_market_two_id_cancel = binary_options_market_two_id_create

    binary_options_market_ids_to_cancel_all = [binary_options_market_one_id_create, binary_options_market_two_id_create]

    binary_options_orders_to_create = [
        composer.BinaryOptionsOrder(
            sender=address.to_acc_bech32(),
            market_id=binary_options_market_one_id_create,
            subaccount_id=subaccount_id,
            fee_recipient=fee_recipient,
            price=price_one,
            quantity=quantity_one,
            is_buy=order_side_one == "buy",
            is_reduce_only=False,
        ),
        composer.BinaryOptionsOrder(
            sender=address.to_acc_bech32(),
            market_id=binary_options_market_one_id_create,
            subaccount_id=subaccount_id,
            fee_recipient=fee_recipient,
            price=price_two,
            quantity=quantity_two,
            is_buy=order_side_two == "buy",
            is_reduce_only=False,
        ),
    ]
    msg = composer.MsgBatchUpdateOrders(
        sender=address.to_acc_bech32(),
        subaccount_id=subaccount_id,
        binary_options_orders_to_create=binary_options_orders_to_create,
        binary_options_market_ids_to_cancel_all=binary_options_market_ids_to_cancel_all,
    )
    return msg


def build_tx(msg, address, network):
    # build sim tx
    tx = (
        Transaction()
        .with_messages(msg)
        .with_sequence(address.get_sequence())
        .with_account_num(address.get_number())
        .with_chain_id(network.chain_id)
    )
    return tx


def init_num_sequence(address, network, pub_key):
    try:
        address = address.init_num_seq(network.lcd_endpoint)
        return address
    except ValueError as e:
        if len(e.args) == 2 and e.args[1] == 404:
            print(
                "Failed to initialize account {}; account may be missing INJ.".format(
                    pub_key.to_address().to_acc_bech32()
                )
            )
        else:
            raise


async def simulate_and_send_tx(client, composer, network, address, pub_key, tx, retry_attempt):
    # simulate tx
    sim_sign_doc = tx.get_sign_doc(pub_key)
    sim_sig = priv_key.sign(sim_sign_doc.SerializeToString())
    sim_tx_raw_bytes = tx.get_tx_data(sim_sig, pub_key)

    (sim_res, success) = await client.simulate_tx(sim_tx_raw_bytes)
    if not success:
        return sim_res

    sim_res_msg = Composer.MsgResponses(sim_res.result.data, simulation=True)
    print("---Simulation Response---")
    print(sim_res_msg)

    gas_price = 500000000
    gas_limit = sim_res.gas_info.gas_used + 20000  # add 20k for gas, fee computation
    gas_fee = "{:.18f}".format((gas_price * gas_limit) / pow(10, 18)).rstrip("0")
    fee = [
        composer.Coin(
            amount=gas_price * gas_limit,
            denom=network.fee_denom,
        )
    ]
    tx = tx.with_gas(gas_limit).with_fee(fee).with_memo("").with_timeout_height(client.timeout_height)
    sign_doc = tx.get_sign_doc(pub_key)
    sig = priv_key.sign(sign_doc.SerializeToString())
    tx_raw_bytes = tx.get_tx_data(sig, pub_key)

    # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
    res = await client.send_tx_sync_mode(tx_raw_bytes)
    print("---Transaction Response---")
    print(res)
    print("gas wanted: {}".format(gas_limit))
    print("gas fee: {} INJ".format(gas_fee))
    return None


def parse_cli_argments() -> Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("market_one", help="market one name ABC-XYZ")
    parser.add_argument("side_one", help="market one order side: buy or sell")
    parser.add_argument("price_one", type=float, help="market one order price, float")
    parser.add_argument("quantity_one", type=int, help="market one order quantity, int")

    parser.add_argument("market_two", help="market two name ABC-XYZ")
    parser.add_argument("side_two", help="market two order side: buy or sell")
    parser.add_argument("price_two", type=float, help="market two order price, float")
    parser.add_argument("quantity_two", type=int, help="market two order quantity, int")
    args = parser.parse_args()
    return args


def get_env_variable(env_name: str) -> str:
    # Checking the value of the environment variable
    env_value = environ.get(env_name)
    if env_value:
        return env_value
    else:
        print(f"{env_name} is off")
        sys.exit(1)


def is_multi_states_market(market_name: str) -> bool:
    if market_name in []:
        return True
    else:
        return False


def get_market_id(market_name: str, order_side: str) -> str:
    if is_multi_states_market(market_name):
        return "0x2f47a461721b3f3e2cd10bac46cea89b22d80fa2d049b3f7654ba9f56917c169"
    else:
        return "0x2f47a461721b3f3e2cd10bac46cea89b22d80fa2d049b3f7654ba9f56917c169"


if __name__ == "__main__":
    namespace = parse_cli_argments()

    priv_key = PrivateKey.from_hex(get_env_variable("INJ_PRIVATE_KEY"))
    fee_recipient = get_env_variable("INJ_ADDRESS")
    asyncio.get_event_loop().run_until_complete(
        run(
            namespace.market_one,
            namespace.side_one,
            namespace.price_one,
            namespace.quantity_one,
            namespace.market_two,
            namespace.side_two,
            namespace.price_two,
            namespace.quantity_two,
        )
    )
