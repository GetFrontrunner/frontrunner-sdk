import logging

from typing import cast
from typing import Iterable
from typing import List
from typing import Tuple

from google.protobuf.message import Message
from grpc.aio import AioRpcError
from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Denom
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import SimulationResponse # NOQA
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse # NOQA
from pyinjective.transaction import Coin
from pyinjective.transaction import Transaction

from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.logging.log_external_exceptions import log_external_exceptions # NOQA
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet

logger = logging.getLogger(__name__)


class InjectiveChain:

  # TODO these are made up numbers
  GAS_PRICE = 500_000_000
  ADDITIONAL_GAS_FEE = 20_000

  DENOM = Denom(
    description="Frontrunner",
    base=0,
    quote=6,

    # 1¢ in satoshis
    min_price_tick_size=10_000,

    # can't go below 1¢
    min_quantity_tick_size=1,
  )

  def __init__(self, composer: Composer, client: AsyncClient, network: Network):
    self.composer = composer
    self.client = client
    self.network = network

  @classmethod
  def _sign_transaction(clz, wallet: Wallet, transaction: Transaction) -> bytes:
    signing_document = transaction.get_sign_doc(wallet.public_key)
    signature = wallet.private_key.sign(signing_document.SerializeToString())
    return transaction.get_tx_data(signature, wallet.public_key)

  def _estimate_fee(self, simulation: SimulationResponse) -> Tuple[int, List[Coin]]:
    limit = int(simulation.gas_info.gas_used) + self.ADDITIONAL_GAS_FEE
    amount = self.GAS_PRICE * limit
    fee = [self.composer.Coin(amount=str(amount), denom=self.network.fee_denom)]
    return (limit, fee)

  def _injective_order_for(self, wallet: Wallet, order: Order) -> Message:
    return self.composer.BinaryOptionsOrder(
      market_id=order.market_id,
      quantity=order.quantity,
      price=order.price,

      # [buy, for]      => [is_buy = True, is_reduce_only = False]
      # [buy, against]  => [is_buy = False, is_reduce_only = False]
      # [sell, for]     => [is_buy = False, is_reduce_only = True]
      # [sell, against] => [is_buy = True, is_reduce_only = True]
      is_buy=((order.direction == "buy") == (order.side == "for")),
      is_reduce_only=(order.direction == "sell"),

      # TODO allow different fee recipient address
      fee_recipient=wallet.injective_address,

      # use default subaccount; can revisit this later
      subaccount_id=wallet.subaccount_address(),

      # We need to specify a placeholder denom because one isn't hardcoded for
      # our ephemeral markets.
      denom=self.DENOM,
    )

  async def _simulate_transaction(self, wallet: Wallet, sequence: int, messages: List[Message]) -> SimulationResponse:
    transaction = self._sign_transaction(
      wallet,
      Transaction(
        msgs=messages,
        sequence=sequence,
        account_num=wallet.account_number,
        chain_id=self.network.chain_id,
      )
    )

    logger.debug(
      "Calling Injective chain to simulate transaction with messages=%s account=%s sequence=%s chain_id=%s",
      str(messages),
      wallet.account_number,
      wallet.sequence,
      self.network.chain_id,
    )

    result, success = await self.client.simulate_tx(transaction)

    if not success:
      cause = cast(AioRpcError, result)
      raise FrontrunnerInjectiveException(
        "Simulation failed",
        code=cause.code(),
        message=cause.debug_error_string(),
        details=cause.details(),
      ) from cause

    response = cast(SimulationResponse, result)

    logger.debug("Received simulation response from Injective chain yielding response=%s", response)

    return response

  async def _send_transaction(
    self,
    wallet: Wallet,
    sequence: int,
    messages: List[Message],
    gas: int,
    fee: List[Coin],
  ) -> TxResponse:
    transaction = self._sign_transaction(
      wallet,
      Transaction(
        msgs=messages,
        sequence=sequence,
        account_num=wallet.account_number,
        chain_id=self.network.chain_id,
        gas=gas,
        fee=fee,
      )
    )

    logger.debug(
      "Calling Injective chain to send sync transaction with messages=%s account=%s chain_id=%s gas=%d fee=%d",
      str(messages),
      wallet.account_number,
      self.network.chain_id,
      gas,
      fee,
    )

    response = await self.client.send_tx_sync_mode(transaction)

    logger.debug("Received transaction response from Injective chain yielding response=%s", response)

    if response.code > 0:
      raise FrontrunnerInjectiveException("Transaction failed", message=response.raw_log)

    return response

  async def _execute_transaction(self, wallet: Wallet, messages: List[Message]) -> TxResponse:
    sequence = wallet.get_and_increment_sequence()
    simulation = await self._simulate_transaction(wallet, sequence, messages)
    gas, fee = self._estimate_fee(simulation)
    return await self._send_transaction(wallet, sequence, messages, gas, fee)

  @log_external_exceptions(__name__)
  async def get_all_open_orders(
    self,
    wallet: Wallet,
  ):
    results = []
    skip = 0
    while True:
      temp_result = await self.client.get_derivative_subaccount_orders(
        wallet.subaccount_address(), skip=skip, limit=100
      )
      if not temp_result or not temp_result.orders or len(temp_result.orders) == 0:
        break
      results.extend(temp_result.orders)
      skip += len(temp_result.orders)
      if temp_result.paging.to == temp_result.paging.total:
        break

    return results

  @log_external_exceptions(__name__)
  async def create_orders(
    self,
    wallet: Wallet,
    orders: Iterable[Order],
  ) -> TxResponse:
    order_messages = [self._injective_order_for(wallet, order) for order in orders]

    batch_message = self.composer.MsgBatchUpdateOrders(
      wallet.injective_address,
      binary_options_orders_to_create=order_messages,
    )

    return await self._execute_transaction(wallet, [batch_message])

  @log_external_exceptions(__name__)
  async def cancel_all_orders_for_markets(
          self,
          wallet: Wallet,
          injective_market_ids: List[str],
  ) -> TxResponse:
    injective_market_ids = list({id for id in injective_market_ids})
    batch_message = self.composer.MsgBatchUpdateOrders(
      wallet.injective_address,
      subaccount_id=wallet.subaccount_address(),
      binary_options_market_ids_to_cancel_all=injective_market_ids,
    )

    return await self._execute_transaction(wallet, [batch_message])
