from configparser import ConfigParser

from typing import List, Optional

from asyncio import get_event_loop, set_event_loop_policy
from uvloop import EventLoopPolicy

import pyinjective
from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network
from pyinjective.composer import Composer
from pyinjective.transaction import Transaction
from pyinjective.wallet import PrivateKey  # , Address


# Grant permission to Grantee
class Granter:
    def __init__(
        self,
        private_key: str,
        grantee_address: str,
        node: str = "sentry0",
        insecure=True,
        is_testnet=False,
    ):
        # select network: mainnet
        if is_testnet:
            self.network = Network.testnet()
            insecure = False
        else:
            self.network = Network.mainnet(node)
        self.composer = Composer(network=self.network.string())

        # initialize grpc client
        self.client = AsyncClient(self.network, insecure=insecure)

        # load account
        self.priv_key = PrivateKey.from_hex(private_key)
        self.pub_key = self.priv_key.to_public_key()
        self.address = self.pub_key.to_address().init_num_seq(self.network.lcd_endpoint)
        self.inj_address = self.address.to_acc_bech32()
        self.grantee_address = grantee_address
        print("inj_address: ", self.inj_address)
        self.subaccount_id = self.address.get_subaccount_id(index=0)
        self.gas_price = 500000000
        self.market_type = "derivative"
        # key is grantee address, values are  list of [permission]
        self.subaccount_balance = {}
        self.is_testnet = is_testnet
        self.binary_permissions = [
            "/injective.exchange.v1beta1.MsgCreateBinaryOptionsLimitOrder",
            "/injective.exchange.v1beta1.MsgCreateBinaryOptionsMarketOrder",
            "/injective.exchange.v1beta1.MsgCancelBinaryOptionsOrder",
            "/injective.exchange.v1beta1.MsgAdminUpdateBinaryOptionsMarket",
            "/injective.exchange.v1beta1.MsgInstantBinaryOptionsMarketLaunch",
        ]

    async def grant_permissions(self):
        msgs = await self._build_grant_permissions_message()
        await self._send_transaction(msgs)

    async def revoke_permissions(self):
        msgs = await self._build_revoke_permissions_message()
        await self._send_transaction(msgs)

    async def _simulate_transcation(self, tx: Transaction) -> Optional[int]:
        sim_sign_doc = tx.get_sign_doc(self.pub_key)
        sim_sig = self.priv_key.sign(sim_sign_doc.SerializeToString())
        sim_tx_raw_bytes = tx.get_tx_data(sim_sig, self.pub_key)

        # simulate tx
        (sim_res, success) = await self.client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            return None
        # sim_res_msg = Composer.MsgResponses(sim_res.result.data, simulation=True)
        return sim_res.gas_info.gas_used

    async def _send_transaction(self, msgs: List):
        tx = (
            Transaction()
            .with_messages(*msgs)
            .with_sequence(self.address.get_sequence())
            .with_account_num(self.address.get_number())
            .with_chain_id(self.network.chain_id)
        )

        gas_used = await self._simulate_transcation(tx)

        if gas_used is None:
            gas_limit = 165000
        else:
            gas_limit = gas_used + 18000

        fee = [
            self.composer.Coin(
                amount=self.gas_price * gas_limit,
                denom=self.network.fee_denom,
            )
        ]

        block = await self.client.get_latest_block()

        # add gas and fee to tx
        tx = (
            tx.with_gas(gas_limit)
            .with_fee(fee)
            .with_memo("")
            .with_timeout_height(block.block.header.height + 50)
        )

        sign_doc = tx.get_sign_doc(self.pub_key)
        sig = self.priv_key.sign(sign_doc.SerializeToString())
        tx_raw_bytes = tx.get_tx_data(sig, self.pub_key)

        # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
        res = await self.client.send_tx_block_mode(tx_raw_bytes)
        # print(res)
        res_msg = self.composer.MsgResponses(res.data)
        print(f"{self.inj_address} grant permission to {self.grantee_address}")
        for (permission, reps) in zip(self.binary_permissions, res_msg):
            if reps.ByteSize() == 0:
                print(f"granted permission: {permission.split('.')[-1]}")
            else:
                print(f"failed to grant permission : {permission.split('.')[-1]}")

    async def _build_grant_permissions_message(self) -> List:

        grant_msgs = []
        print("grant binary options permissions")
        grantee_msgs = [
            self.composer.MsgGrantGeneric(
                granter=self.inj_address,
                grantee=self.grantee_address,
                msg_type=permission,
                expire_in=31536000,  # 1 year
            )
            for permission in self.binary_permissions
        ]
        grant_msgs.extend(grantee_msgs)

        return grant_msgs

    async def _build_revoke_permissions_message(self) -> List:
        revoke_msgs = [
            self.composer.MsgRevoke(
                granter=self.inj_address,
                grantee=self.grantee_address,
                msg_type=permission,
            )
            for permission in self.binary_permissions
        ]

        return revoke_msgs


if __name__ == "__main__":
    import os

    # from dotenv import load_dotenv
    # load_dotenv()
    # Getting non-existent keys
    grantee_private_key = os.getenv("grantee_private_key")  # None
    grantee_inj_address = os.getenv("grantee_inj_address")  # None

    granter_private_key = os.getenv("granter_private_key")  # None
    granter_inj_address = os.getenv("granter_inj_address")  # None

    data = {
        "grantee": {
            "inj_address": grantee_inj_address,
            "priv_key": grantee_private_key,
        },
        "granter": {
            "priv_key": granter_private_key,
            "inj_address": granter_inj_address,
        },
    }

    for account, info in data.items():
        if info["inj_address"] is None:
            raise ValueError(f"{account} address is not set")
        if account == "granter":
            if info["priv_key"] is None:
                raise ValueError(f"{account} private key is not set")

    if data["grantee"]["inj_address"] is not None:
        for account, info in data.items():
            if account != "grantee":
                print("=========================", account, "=========================")
                if info["priv_key"] is not None:
                    granter = Granter(
                        info["priv_key"],
                        grantee_address=data["grantee"]["inj_address"],
                        insecure=True,
                        is_testnet=True,
                    )

                    loop = get_event_loop()
                    set_event_loop_policy(EventLoopPolicy())
                    loop.set_debug(False)
                    loop.set_exception_handler(lambda _, ctx: print(ctx))

                    loop.run_until_complete(granter.grant_permissions())
