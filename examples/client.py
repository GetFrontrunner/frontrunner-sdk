import os
import logging
from enum import Enum
from typing import Optional, Tuple, Union, Any, List, Dict
from asyncio import Lock

import grpc
from google.protobuf.message import Message
from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer as ProtoMsgComposer
from pyinjective.constant import Network, Denom
from pyinjective.transaction import Transaction
from pyinjective.wallet import PrivateKey, Address, PublicKey

from pyinjective.proto.cosmos.base.abci.v1beta1 import abci_pb2
from pyinjective.proto.cosmos.base.v1beta1 import coin_pb2 as cosmos_base_coin_pb
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse
from pyinjective.proto.injective.exchange.v1beta1 import tx_pb2 as injective_exchange_tx_pb

from generate_account import generate_mnemonic, set_env_variables, check_env_is_on, request_test_tokens

# from common.injective_client.src.injective_composer import InjectiveComposer


logger = logging.getLogger(__name__)

DEFAULT_GAS_PRICE = 500000000
DEFAULT_COMPUTATION_GAS = 20000
MAX_INJECTIVE_RETRY_ATTEMPTS = 5
BINARY_OPTIONS_DEFAULT_PROVIDER = "Frontrunner"
DEFAULT_FILE_LOCATION = "examples.env"


class BroadcastMode(Enum):
    ASYNC = 0
    SYNC = 1
    BLOCK = 2


class CustomNetwork:
    def __init__(
        self,
        lcd_endpoint: str,
        tm_endpoint: str,
        grpc_endpoint: str,
        exchange_endpoint: str,
        mainnet=False,
        mainnet_node="k8s",
    ):
        self.lcd_endpoint = lcd_endpoint
        self.source_network = Network.mainnet(mainnet_node) if mainnet else Network.testnet()
        self._network = Network(
            lcd_endpoint=lcd_endpoint,
            tm_websocket_endpoint=f"ws://{tm_endpoint}/websocket",
            grpc_endpoint=grpc_endpoint,
            grpc_exchange_endpoint=exchange_endpoint,
            grpc_explorer_endpoint=self.source_network.grpc_explorer_endpoint,
            # TODO: use Injective's API until we can run our own explorer container
            chain_id=self.source_network.chain_id,
            fee_denom=self.source_network.fee_denom,
            env=self.source_network.env,
        )

    @property
    def network(self) -> Network:
        return self._network


class InjectiveExchangeClient:
    def __init__(
        self,
        mainnet: bool = False,
        node: Optional[str] = None,
        override_network: Optional[bool] = None,
        insecure: bool = False,
        max_injective_retry_attempts: int = MAX_INJECTIVE_RETRY_ATTEMPTS,
        chain_cookie_location: str = "/tmp/.chain_cookie",
    ):
        """
        A wrapped Injective client for interacting with the read-only Exchange API: https://api.injective.exchange/#exchange-api
        :param mainnet: if false, connect to Testnet
        :param node: Sentry node to connect to https://api.injective.exchange/#faq-4-which-api-nodes-can-i-connect-to
        :param override_network: Injective Network to connect to (overrides other network-related params)
        :param insecure: insecure is ok, since all operations are public on the blockchain
        :param chain_cookie_location: if passed in, must be on version >= 0.5.7.4 that has the new input (and should be /tmp/.chain_cookie).
            Temporary until all clients are moved to the new version.
        """
        self.network: Network = (
            override_network if override_network else Network.mainnet(node=node) if mainnet else Network.testnet()
        )  # NOTE testnet does not support the node option anymore
        logger.debug(f"Initializing Injective client with network: {self.network.__dict__} and {insecure=}")
        self._insecure: bool = insecure
        self._chain_cookie_location: str = chain_cookie_location
        self._async_client: AsyncClient = AsyncClient(
            self.network, insecure=insecure, chain_cookie_location=self._chain_cookie_location
        )
        self._max_injective_retry_attempts: int = max_injective_retry_attempts
        self.denom = self._get_default_denom()

    def reset_clients(self):
        self._async_client = AsyncClient(
            self.network, insecure=self._insecure, chain_cookie_location=self._chain_cookie_location
        )

    @property
    def async_client(self) -> AsyncClient:
        return self._async_client

    def get_peggy_denom(self, symbol) -> Tuple[str, int]:
        """
        :param symbol: e.g. USDT
        :return: tuple of peggy denom and decimals e.g. ("peggy0xdAC17F958D2ee523a2206206994597C13D831ec7", 6)
        """
        return Denom.load_peggy_denom(self.network.env, symbol)

    @staticmethod
    def _get_default_denom() -> Denom:
        """
        Normally we should be able to run this, but there is a limitation on the Injective SDK
        where the Denom must be hardcoded in the inj file for each market.
        To work around this, we need to inline the underlying code
        and default the denom parameters to match FR markets.
        :return:
        """
        # defaults for our markets
        # is_po = False  # https://help.bybit.com/hc/en-us/articles/360039749433-What-Is-A-Post-Only-Order-
        denom_min_price_tick_size = 10000
        denom_min_quantity_tick_size = 1
        denom_quote = 6
        denom_base = 0
        denom_desc = "desc"  # this is only logged and not used for any logic-related lookup;
        # avoids a market lookup given our current setup
        denom = Denom(
            description=denom_desc,
            base=denom_base,
            quote=denom_quote,
            min_price_tick_size=denom_min_price_tick_size,
            min_quantity_tick_size=denom_min_quantity_tick_size,
        )
        return denom


class AsyncInjectiveChainClient(InjectiveExchangeClient):
    """
    Async version of the Injective Chain Client.
    """

    def __init__(
        self,
        fee_recipient_address: Optional[str] = None,
        priv_key_hex: Optional[str] = None,
        mnemonic: Optional[str] = None,
        mainnet: bool = False,
        node: Optional[str] = None,
        override_network: Optional[Network] = None,
        insecure: bool = False,
    ):
        """
        A wrapped Injective client for interacting with the writable Chain API: https://api.injective.exchange/#chain-api
        :param fee_recipient_address: address where part of the trading fees get sent https://api.injective.exchange/#overview-trading-fees-and-gas
        :param priv_key_hex: private key of the sender
        :param mnemonic: mnemonic of the sender (overrides priv_key_hex). one of priv_key_hex or mnemonic must be given
        :param mainnet: see InjectiveExchangeClient
        :param node: see InjectiveExchangeClient
        :param override_network: see InjectiveExchangeClient
        :param insecure: see InjectiveExchangeClient
        """
        # NOTE we can't override the default InjectiveChainClient as initializing the sequence number is an async call
        super().__init__(mainnet=mainnet, node=node, override_network=override_network, insecure=insecure)

        self.composer = ProtoMsgComposer(network=self.network.string())

        if not priv_key_hex and not mnemonic:
            print("generate a new account")
            priv_key_hex = self.generate_account()

        self._priv_key: PrivateKey = (
            PrivateKey.from_hex(priv_key_hex) if priv_key_hex else PrivateKey.from_mnemonic(mnemonic)
        )

        self.pub_key: PublicKey = self._priv_key.to_public_key()
        self.sender_address: Address = self.pub_key.to_address()
        self.sender_address_bech32: str = self.sender_address.to_acc_bech32()
        self.subaccount_id: str = self.sender_address.get_subaccount_id(0)
        self.fee_recipient_address: str = fee_recipient_address if fee_recipient_address else self.sender_address_bech32
        self.num_seq_lock = Lock()

    def generate_account(self):
        secret_obj = generate_mnemonic()
        set_env_variables(secret_obj, DEFAULT_FILE_LOCATION)
        os.system(f"bash -c 'cat {DEFAULT_FILE_LOCATION}'")
        os.system(f"bash -c 'source {DEFAULT_FILE_LOCATION}'")
        request_test_tokens(secret_obj["inj_address"])
        print("run 'source .env' to set env variables")
        return secret_obj["inj_private_key"]

    @staticmethod
    def to_inj_subaccount_address(wallet_address) -> str:
        hex_bytes = bytes.fromhex(wallet_address.replace("0x", ""))
        injective_address = Address(hex_bytes)
        return injective_address.to_acc_bech32()

    def _build_batch_msg(
        self, orders_to_create: List[Dict], orders_to_cancel: List[Dict]
    ) -> injective_exchange_tx_pb.MsgBatchUpdateOrders:
        binary_options_orders_to_create = list(
            map(
                lambda order: self.composer.BinaryOptionsOrder(
                    sender=self.sender_address.to_acc_bech32(),
                    market_id=order["market_id"],
                    subaccount_id=order["subaccount_id"],
                    fee_recipient=self.fee_recipient_address,
                    price=order["price"],
                    quantity=order["quantity"],
                    is_buy=order["is_buy"],
                    is_reduce_only=order["is_reduce_only"],
                    is_po=order["is_po"],
                    denom=self.denom,
                ),
                orders_to_create,
            )
        )

        binary_options_orders_to_cancel = list(
            map(
                lambda order: self.composer.OrderData(
                    market_id=order["market_id"], subaccount_id=order["subaccount_id"], order_hash=order["order_hash"]
                ),
                orders_to_cancel,
            )
        )

        msg = self.composer.MsgBatchUpdateOrders(
            sender=self.sender_address_bech32,
            binary_options_orders_to_create=binary_options_orders_to_create,
            binary_options_orders_to_cancel=binary_options_orders_to_cancel,
        )

    async def batch_update_orders(self, orders_to_create: List[Dict], orders_to_cancel: List[Dict]):
        msg = self._build_batch_msg(orders_to_create, orders_to_cancel)

        async with self.num_seq_lock:
            retry_attempt = 1
            while retry_attempt < 3:  # Attempt 2 times
                res, sim_res = await self._send_message(msg, retry_attempt=retry_attempt)
                if not res or res.code != 0:  # transaction failed
                    # Assume that it can be an account sequence mismatch or another issue, attempt to retry
                    self._block_init_num_sequence()
                    retry_attempt += 1
                    if retry_attempt < 3:
                        continue
                    if sim_res:
                        raise Exception(
                            str(sim_res._state.details)
                        )  # Return the message from the _InactiveRpcError Error
                if sim_res:
                    return ProtoMsgComposer.MsgResponses(sim_res.result.data, simulation=True)

    def _build_tx(self, msg) -> Transaction:
        # build sim tx
        tx = (
            Transaction()
            .with_messages(msg)
            .with_sequence(self.sender_address.get_sequence())
            .with_account_num(self.sender_address.get_number())
            .with_chain_id(self.network.chain_id)
        )
        return tx

    async def _update_tx(self, tx: Transaction, gas_limit: int, fee: List[cosmos_base_coin_pb.Coin]) -> Transaction:
        latest_block = await self.async_client.get_latest_block()
        current_height = latest_block.block.header.height
        tx = tx.with_gas(gas_limit).with_fee(fee).with_memo("").with_timeout_height(current_height + 50)
        return tx

    def _build_sim_bytes(self, tx):
        sim_sign_doc = tx.get_sign_doc(self.pub_key)
        sim_sig = self._priv_key.sign(sim_sign_doc.SerializeToString())
        sim_tx_raw_bytes = tx.get_tx_data(sim_sig, self.pub_key)
        return sim_tx_raw_bytes

    def _block_init_num_sequence(self):
        try:
            self.sender_address = self.sender_address.init_num_seq(self.network.lcd_endpoint)
        except ValueError as e:
            if len(e.args) == 2 and e.args[1] == 404:
                print(
                    "Failed to initialize account {}; account may be missing INJ.".format(
                        self.pub_key.to_address().to_acc_bech32()
                    )
                )
            else:
                raise

    async def simulate_and_send_tx(self, tx, retry_attempt):
        # simulate tx
        sim_tx_raw_bytes = self._build_sim_bytes(tx)
        (sim_res, success) = await self.async_client.simulate_tx(sim_tx_raw_bytes)
        if not success:
            return sim_res

        sim_res_msg = self.composer.MsgResponses(sim_res.result.data, simulation=True)
        print("---Simulation Response---")
        print(sim_res_msg)

        gas_limit = sim_res.gas_info.gas_used + DEFAULT_COMPUTATION_GAS  # add 20k for gas, fee computation
        fee = self._build_fee(gas_limit)
        tx = await self._update_tx(tx, gas_limit, fee)
        tx_raw_bytes = self._build_sim_bytes(tx)

        # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode
        res = await self.async_client.send_tx_sync_mode(tx_raw_bytes)
        print("---Transaction Response---")
        print(res)
        return None

    def _build_fee(self, gas_limit) -> List[cosmos_base_coin_pb.Coin]:
        gas_fee = "{:.18f}".format((DEFAULT_GAS_PRICE * gas_limit) / pow(10, 18)).rstrip("0")
        fee = [
            self.composer.Coin(
                amount=DEFAULT_GAS_PRICE * gas_limit,
                denom=self.network.fee_denom,
            )
        ]
        logger.debug(f"gas wanted: {gas_limit}; gas fee: {gas_fee} INJ")
        return fee

    async def _send_message(
        self, msg: Message, mode: BroadcastMode = BroadcastMode.BLOCK, retry_attempt: int = 1
    ) -> Tuple[Optional[TxResponse], Optional[Union[abci_pb2.SimulationResponse, grpc.RpcError]]]:

        """
        Convenience wrapper method that sends a message (a.k.a. transaction) to Injective
        :param msg: message created by Composer
        :param mode: Async: don't check txn; Sync: wait for check txn; Block: wait for check, delivery, and commitment in block
        :return: Tuple of transaction response and simulation response/error
        """
        if retry_attempt > self._max_injective_retry_attempts:
            logger.error("Injective max retry attempt exceeded. Retry attempt – {}".format(retry_attempt))
            return None, None
        try:
            tx = self._build_tx(msg)
            sim_tx_raw_bytes = self._build_sim_bytes(tx)

            # simulate tx
            (sim_response_or_error, success) = await self.async_client.simulate_tx(sim_tx_raw_bytes)
            if not success:
                logger.debug("error simulating: {}".format(sim_response_or_error))  # caller should log
                if "account sequence mismatch" in sim_response_or_error.details():
                    self._block_init_num_sequence()
                    return await self._send_message(msg, mode=mode, retry_attempt=retry_attempt + 1)
                else:
                    return None, sim_response_or_error
            logger.debug(f"simulate txn response message: {sim_response_or_error}")

            # build tx, add gas for fee computation
            gas_limit = sim_response_or_error.gas_info.gas_used + DEFAULT_COMPUTATION_GAS
            fee = self._build_fee(gas_limit)

            await self._update_tx(tx, gas_limit, fee)
            tx_raw_bytes = self._build_sim_bytes(tx)
            # broadcast tx: send_tx_async_mode, send_tx_sync_mode, send_tx_block_mode

            tx_response: TxResponse = self._send_txn_with_mode(tx_raw_bytes, mode)
            logger.debug("Transaction response: {}".format(tx_response))

            if tx_response.code != 0:
                logger.error("Injective transaction has failed: ", tx_response)
            return tx_response, sim_response_or_error
        except grpc.RpcError as grpc_error:
            logger.error('GRPC Error happened while executing the message: "{}"'.format(msg), grpc_error)
            if grpc_error.code() == grpc.StatusCode.UNKNOWN:
                # possible account sequence mismatch, trying to restart the sequence and execute the message again
                self._block_init_num_sequence()
                return await self._send_message(msg, mode=mode, retry_attempt=retry_attempt + 1)
        except Exception:
            logger.exception(f'Exception happened while executing the message: "{msg}"')
        return None, None

    async def _send_txn_with_mode(self, tx_raw_bytes: bytes, mode: BroadcastMode):
        if mode == BroadcastMode.ASYNC:
            return await self.async_client.send_tx_async_mode(tx_raw_bytes)
        elif mode == BroadcastMode.SYNC:
            return await self.async_client.send_tx_sync_mode(tx_raw_bytes)
        elif mode == BroadcastMode.BLOCK:
            return await self.async_client.send_tx_block_mode(tx_raw_bytes)
        else:
            raise ValueError(f"Unsupported mode: {mode.name}")


def async_injective_chain_client_factory(
    lcd_endpoint: Optional[str] = None,
    tm_endpoint: Optional[str] = None,
    grpc_endpoint: Optional[str] = None,
    exchange_endpoint: Optional[str] = None,
    mainnet: bool = False,
    node: Optional[str] = None,
    insecure: bool = False,
    fee_recipient_address: Optional[str] = "",
):
    if lcd_endpoint and tm_endpoint and grpc_endpoint and exchange_endpoint:
        print("using custom network")
        custom_network = CustomNetwork(lcd_endpoint, tm_endpoint, grpc_endpoint, exchange_endpoint, mainnet=mainnet)
        network = custom_network.network
        return AsyncInjectiveChainClient(
            fee_recipient_address=fee_recipient_address, override_network=network, insecure=insecure
        )
    else:
        print("using default network")

    return AsyncInjectiveChainClient(
        fee_recipient_address=fee_recipient_address, mainnet=mainnet, node=node, insecure=insecure
    )
