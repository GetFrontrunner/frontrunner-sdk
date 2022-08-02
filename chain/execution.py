import logging

# from security_module import batch_compute_order_hashes
from pyinjective.transaction import Transaction
from pyinjective.wallet import Address, PublicKey, PrivateKey
from pyinjective.composer import Composer
from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network  # , Denom
from utils.granter import Granter
from typing import List, Any


"""
def build_replace_orders_msgs(
    composer: Composer,
    granters: List[Granter],
    inj_address: str,
):
    replace_msgs_list = []
    for granter in granters:
        perp_orders = gather_perp_orders(granter)
        spot_orders = gather_spot_orders(granter)
        replace_msgs_list.append(
            composer.MsgBatchUpdateOrders(
                sender=inj_address,
                subaccount_id=granter.subaccount_id,
                derivative_orders_to_create=perp_orders
                if len(perp_orders) > 0
                else None,
                spot_orders_to_create=spot_orders if len(spot_orders) > 0 else None,
                derivative_market_ids_to_cancel_all=[
                    market.market_id
                    if market.market_type == "perp"
                ],
                spot_market_ids_to_cancel_all=[
                    market.market_id
                    for market in granter.markets.values()
                    if market.market_type == "spot"
                ],
            )
        )

    return composer.MsgExec(grantee=inj_address, msgs=replace_msgs_list)


def gather_spot_orders(granter: Granter):
    bid_order_msgs = [
        order.msg
        for market in granter.markets.values()
        if market.market_type == "spot"
        for order in market.bid_orders
    ]
    ask_order_msgs = [
        order.msg
        for market in granter.markets.values()
        if market.market_type == "spot"
        for order in market.ask_orders
    ]
    return bid_order_msgs + ask_order_msgs


def gather_perp_orders(granter: Granter):
    bid_order_msgs = [
        order.msg
        for market in granter.markets.values()
        if market.market_type == "perp"
        for order in market.bid_orders
    ]
    ask_order_msgs = [
        order.msg
        for market in granter.markets.values()
        if market.market_type == "perp"
        for order in market.ask_orders
    ]
    return bid_order_msgs + ask_order_msgs

"""


async def execute(
    pub_key: PublicKey,
    priv_key: PrivateKey,
    address: Address,
    network: Network,
    client: AsyncClient,
    composer: Composer,
    gas_price: int,
    msgs: List[Any],
    send_mode: str = "block",
    update_sequence: bool = True,
):
    if not update_sequence:
        seq = address.get_sequence()
    else:
        seq = address.init_num_seq(network.lcd_endpoint).get_sequence()

    tx = (
        Transaction()
        .with_messages(msgs)
        .with_sequence(seq)
        .with_account_num(address.get_number())
        .with_chain_id(network.chain_id)
    )

    sim_sign_doc = tx.get_sign_doc(pub_key)
    sim_sig = priv_key.sign(sim_sign_doc.SerializeToString())
    sim_tx_raw_bytes = tx.get_tx_data(sim_sig, pub_key)

    # simulate tx
    (sim_res, success) = await client.simulate_tx(sim_tx_raw_bytes)
    if not success:
        logging.error(f"failed simulation: {sim_res}")

    sim_res_msg = Composer.MsgResponses(sim_res.result.data, simulation=True)
    if sim_res_msg is None:
        logging.error(f"simulation result: {sim_res_msg}")
        return

    gas_limit = sim_res.gas_info.gas_used + 20000

    fee = [
        composer.Coin(
            amount=gas_price * gas_limit,
            denom=network.fee_denom,
        )
    ]

    # add gas and fee to tx
    tx = tx.with_gas(gas_limit).with_fee(fee).with_memo("")

    sign_doc = tx.get_sign_doc(pub_key)
    sig = priv_key.sign(sign_doc.SerializeToString())
    tx_raw_bytes = tx.get_tx_data(sig, pub_key)

    # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
    try:
        # res = await self.client.send_tx_block_mode(tx_raw_bytes)
        if send_mode == "async":
            res = await client.send_tx_async_mode(tx_raw_bytes)
        elif send_mode == "sync":
            res = await client.send_tx_sync_mode(tx_raw_bytes)
        else:
            res = await client.send_tx_block_mode(tx_raw_bytes)
    except Exception as e:
        logging.error(f"broadcast error: {e}")
        return

    # logging.debug("type res: ", type(res)) FIXME need to check gas
    res_msg = composer.MsgResponses(res.data)
    if len(res_msg) == 0:
        address.get_sequence()
        logging.debug(f"res: {res}")
    return res_msg
