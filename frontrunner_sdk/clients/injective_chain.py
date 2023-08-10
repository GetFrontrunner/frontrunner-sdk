import asyncio
import logging

from collections import defaultdict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple

from google.protobuf.message import Message
from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Denom
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import SimulationResponse # NOQA
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse
from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder # NOQA
from pyinjective.transaction import Coin
from pyinjective.transaction import Transaction

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.helpers.paginators import injective_paginated_list
from frontrunner_sdk.logging.log_external_exceptions import log_external_exceptions # NOQA
from frontrunner_sdk.models.cancel_order import CancelOrder
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Subaccount
from frontrunner_sdk.models.wallet import Wallet

logger = logging.getLogger(__name__)


class InjectiveChain:

  LOCKS = defaultdict(asyncio.Lock)

  # TODO these are made up numbers
  GAS_PRICE = 500_000_000

  DENOM = Denom(
    description="Frontrunner",
    base=0,
    quote=6,

    # 1¢ in satoshis
    min_price_tick_size=10_000,

    # can't go below 1¢
    min_quantity_tick_size=1,
  )

  def __init__(self, composer: Composer, client: AsyncClient, network: Network, gas_estimator: GasEstimator):
    self.composer = composer
    self.client = client
    self.network = network
    self.fee_estimator = gas_estimator

  async def _estimate_cost(self, messages: List[Message]) -> Tuple[int, List[Coin]]:
    gas = sum(await asyncio.gather(*[self.fee_estimator.gas_for(message) for message in messages]))
    fee = [self.composer.Coin(amount=self.GAS_PRICE * gas, denom=self.network.fee_denom)]
    return gas, fee

  def _injective_order(self, wallet: Wallet, order: Order) -> Message:
    return self.composer.BinaryOptionsOrder(
      market_id=order.market_id,
      quantity=order.quantity,
      price=order.price,

      # [buy, long]   => [is_buy = True,  is_reduce_only = False]
      # [buy, short]  => [is_buy = False, is_reduce_only = False]
      # [sell, long]  => [is_buy = False, is_reduce_only = True]
      # [sell, short] => [is_buy = True,  is_reduce_only = True]
      is_buy=((order.direction == "buy") == (order.side == "long")),
      is_reduce_only=(order.direction == "sell"),

      # a post-only order will only succeed if it enters the orderbook unmatched
      is_po=order.is_post_only,

      # TODO allow different fee recipient address
      fee_recipient=wallet.injective_address,

      # uses default subaccount if not set explicitly on the order
      subaccount_id=wallet.subaccount_address(order.subaccount_index),

      # We need to specify a placeholder denom because one isn't hardcoded for
      # our ephemeral markets.
      denom=self.DENOM,
    )

  def _injective_order_cancel(self, wallet: Wallet, market_id: str, order_hash: str, subaccount_index: int):
    return self.composer.OrderData(
      market_id=market_id, subaccount_id=wallet.subaccount_address(subaccount_index), order_hash=order_hash
    )

  async def _send_transaction(
    self,
    wallet: Wallet,
    messages: List[Message],
    gas: int,
    fee: List[Coin],
  ) -> TxResponse:
    async with self.LOCKS[wallet.injective_address]:
      transaction = Transaction(
        msgs=messages,
        sequence=wallet.sequence,
        account_num=wallet.account_number,
        chain_id=self.network.chain_id,
        gas=gas,
        fee=fee,
      )

      signed = wallet.sign(transaction)

      logger.debug(
        "Calling Injective chain to send sync transaction with messages=%s account=%s sequence=%d chain_id=%s gas=%d fee=%d",
        str(messages),
        wallet.account_number,
        wallet.sequence,
        self.network.chain_id,
        gas,
        fee,
      )

      response = await self.client.send_tx_sync_mode(signed)

      logger.debug("Received transaction response from Injective chain yielding response=%s", response)

      if response.code > 0:
        raise FrontrunnerInjectiveException("Transaction failed", message=response.raw_log)

      else:
        wallet.get_and_increment_sequence()

      return response

  async def _execute_transaction(self, wallet: Wallet, messages: List[Message]) -> TxResponse:
    gas, fee = await self._estimate_cost(messages)
    return await self._send_transaction(wallet, messages, gas, fee)

  @log_external_exceptions(__name__)
  async def get_all_open_orders(self, subaccount: Subaccount) -> Iterable[DerivativeLimitOrder]:
    return await injective_paginated_list(
      self.client.get_derivative_subaccount_orders,
      "orders",
      subaccount.subaccount_id,
    )

  @log_external_exceptions(__name__)
  async def create_orders(
    self,
    wallet: Wallet,
    orders: Iterable[Order],
  ) -> TxResponse:
    order_messages = [self._injective_order(wallet, order) for order in orders]

    batch_message = self.composer.MsgBatchUpdateOrders(
      wallet.injective_address,
      binary_options_orders_to_create=order_messages,
    )

    return await self._execute_transaction(wallet, [batch_message])

  @log_external_exceptions(__name__)
  async def cancel_all_orders_for_markets(
    self,
    wallet: Wallet,
    subaccount: Subaccount,
    injective_market_ids: Set[str],
  ) -> TxResponse:
    batch_message = self.composer.MsgBatchUpdateOrders(
      wallet.injective_address,
      subaccount_id=subaccount.subaccount_id,
      binary_options_market_ids_to_cancel_all=injective_market_ids,
    )

    return await self._execute_transaction(wallet, [batch_message])

  @log_external_exceptions(__name__)
  async def cancel_orders(self, wallet: Wallet, orders: Iterable[CancelOrder]) -> TxResponse:
    order_messages = [
      self._injective_order_cancel(wallet, order.market_id, order.order_hash, order.subaccount_index)
      for order in orders
      if order.order_hash
    ]

    batch_message = self.composer.MsgBatchUpdateOrders(
      wallet.injective_address,
      binary_options_orders_to_cancel=order_messages,
    )

    return await self._execute_transaction(wallet, [batch_message])

  @log_external_exceptions(__name__)
  async def fund_external_subaccount(
    self, wallet: Wallet, source_subaccount_id: str, destination_subaccount_id: str, amount: int, denom: str
  ) -> TxResponse:
    message = self.composer.MsgExternalTransfer(
      wallet.injective_address,
      source_subaccount_id=source_subaccount_id,
      destination_subaccount_id=destination_subaccount_id,
      amount=amount,
      denom=denom,
    )

    return await self._execute_transaction(wallet, [message])

  @log_external_exceptions(__name__)
  async def fund_external_wallet_from_bank(
    self, wallet: Wallet, to_address: str, amount: int, denom: str
  ) -> TxResponse:
    message = self.composer.MsgSend(
      wallet.injective_address,
      to_address=to_address,
      amount=amount,
      denom=denom,
    )

    return await self._execute_transaction(wallet, [message])

  @log_external_exceptions(__name__)
  async def fund_subaccount_from_bank(self, wallet: Wallet, subaccount_id: str, amount: int, denom: str) -> TxResponse:
    message = self.composer.MsgDeposit(
      wallet.injective_address,
      subaccount_id=subaccount_id,
      amount=amount,
      denom=denom,
    )

    return await self._execute_transaction(wallet, [message])

  @log_external_exceptions(__name__)
  async def fund_subaccount_from_subaccount(
    self, wallet: Wallet, source_subaccount_id: str, destination_subaccount_id: str, amount: int, denom: str
  ) -> TxResponse:
    message = self.composer.MsgSubaccountTransfer(
      wallet.injective_address,
      source_subaccount_id=source_subaccount_id,
      destination_subaccount_id=destination_subaccount_id,
      amount=amount,
      denom=denom,
    )

    return await self._execute_transaction(wallet, [message])

  @log_external_exceptions(__name__)
  async def withdraw_from_subaccount(self, wallet: Wallet, subaccount_id: str, amount: int, denom: str) -> TxResponse:
    message = self.composer.MsgWithdraw(
      wallet.injective_address,
      subaccount_id=subaccount_id,
      amount=amount,
      denom=denom,
    )

    return await self._execute_transaction(wallet, [message])
