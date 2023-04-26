from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from grpc import StatusCode
from grpc.aio import AioRpcError
from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import GasInfo # NOQA
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import SimulationResponse # NOQA
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderInfo
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderType
from pyinjective.transaction import Transaction
from pyinjective.utils import derivative_price_to_backend
from pyinjective.utils import derivative_quantity_to_backend

from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveChain(IsolatedAsyncioTestCase):

  def setUp(self):
    self.wallet = Wallet._new()

    self.order = DerivativeOrder(
      trigger_price="0",
      margin="4500000",
      market_id="<market-id>",
      order_type="BUY",
      order_info=OrderInfo(
        fee_recipient="<sender>",
        price="500000",
        quantity="10",
        subaccount_id="<subaccount>",
      ),
    )

    self.transaction = Transaction(
      msgs=[self.order],
      sequence=1,
      account_num=1234,
      chain_id="<chain-id>",
    )

    self.client = MagicMock(spec=AsyncClient)
    self.network = MagicMock(spec=Network)
    self.composer = MagicMock(wraps=Composer(self.network))
    self.injective_chain = InjectiveChain(self.composer, self.client, self.network)

    self.network.fee_denom = "inj"
    self.network.chain_id = "<chain-id>"

  def test_sign_transaction(self):
    signed_transaction = InjectiveChain._sign_transaction(self.wallet, self.transaction)

    public_key = self.wallet.public_key
    signature = self.wallet.private_key.signing_key.to_der()

    public_key.verify(signed_transaction, signature)

  def test_estimate_fee(self):
    simulation = SimulationResponse(gas_info=GasInfo(gas_used=1000))

    limit, fee = self.injective_chain._estimate_fee(simulation)

    self.assertEqual(limit, 1000 + InjectiveChain.ADDITIONAL_GAS_FEE)
    self.assertEqual(fee[0].amount, str(InjectiveChain.GAS_PRICE * (1000 + InjectiveChain.ADDITIONAL_GAS_FEE)))

  def test_injective_order_generic(self):
    order = self.injective_chain._injective_order(self.wallet, Order.buy_long("<market-id>", 7, 0.25))

    self.assertEqual(order.market_id, "<market-id>")
    self.assertEqual(order.order_info.quantity, str(derivative_quantity_to_backend(7, InjectiveChain.DENOM)))
    self.assertEqual(order.order_info.price, str(derivative_price_to_backend(0.25, InjectiveChain.DENOM)))

    self.assertEqual(order.order_info.fee_recipient, self.wallet.injective_address)
    self.assertEqual(order.order_info.subaccount_id, self.wallet.subaccount_address())

  def test_injective_order_combinations(self):
    buy_long = self.injective_chain._injective_order(self.wallet, Order.buy_long("<market-id>", 1, 0.5))

    self.assertEqual(buy_long.order_type, OrderType.BUY)
    self.assertNotEqual(int(buy_long.margin), 0)

    buy_short = self.injective_chain._injective_order(self.wallet, Order.buy_short("<market-id>", 1, 0.5))

    self.assertEqual(buy_short.order_type, OrderType.SELL)
    self.assertNotEqual(int(buy_short.margin), 0)

    sell_long = self.injective_chain._injective_order(self.wallet, Order.sell_long("<market-id>", 1, 0.5))

    self.assertEqual(sell_long.order_type, OrderType.SELL)
    self.assertEqual(int(sell_long.margin), 0)

    sell_short = self.injective_chain._injective_order(self.wallet, Order.sell_short("<market-id>", 1, 0.5))

    self.assertEqual(sell_short.order_type, OrderType.BUY)
    self.assertEqual(int(sell_short.margin), 0)

  async def test_simulate_transaction_success(self):
    expected = SimulationResponse()

    self.client.simulate_tx = AsyncMock(return_value=(expected, True))

    response = await self.injective_chain._simulate_transaction(self.wallet, 0, [self.order])

    self.assertEqual(expected, response)

  async def test_simulate_transaction_failure(self):
    self.client.simulate_tx = AsyncMock(return_value=(AioRpcError(StatusCode.UNKNOWN, None, None), False))

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_chain._simulate_transaction(self.wallet, 0, [self.order])

  async def test_send_transaction_success(self):
    expected = TxResponse(code=0)
    self.client.send_tx_sync_mode = AsyncMock(return_value=expected)

    response = await self.injective_chain._send_transaction(self.wallet, 0, [self.order], 100, [])

    self.assertEqual(expected, response)

  async def test_send_transaction_failure(self):
    expected = TxResponse(code=7, raw_log="boom")
    self.client.send_tx_sync_mode = AsyncMock(return_value=expected)

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_chain._send_transaction(self.wallet, 0, [self.order], 100, [])

  async def test_execute_transaction(self):
    simulation = MagicMock(spec=SimulationResponse)
    expected = MagicMock(spec=TxResponse)

    self.injective_chain._simulate_transaction = AsyncMock(return_value=simulation)
    self.injective_chain._estimate_fee = MagicMock(return_value=(5, []))
    self.injective_chain._send_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain._execute_transaction(self.wallet, [self.order])

    self.assertEqual(expected, response)
    self.assertEqual(1, self.wallet.sequence)

    self.injective_chain._simulate_transaction.assert_awaited_once()
    self.injective_chain._send_transaction.assert_awaited_once()

  async def test_create_orders(self):
    expected = MagicMock(spec=TxResponse)
    self.injective_chain._execute_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain.create_orders(self.wallet, [Order.buy_long("<market-id>", 1, 0.5)])

    self.assertEqual(expected, response)

    self.injective_chain._execute_transaction.assert_awaited_once()

    message = self.injective_chain._execute_transaction.call_args.args[1][0]

    self.assertIsNotNone(message.binary_options_orders_to_create)

  async def test_cancel_all_orders_for_markets(self):
    expected = MagicMock(spec=TxResponse)
    self.injective_chain._execute_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain.cancel_all_orders_for_markets(self.wallet, ["<market-id>"])

    self.assertEqual(expected, response)

    self.injective_chain._execute_transaction.assert_awaited_once()

    message = self.injective_chain._execute_transaction.call_args.args[1][0]

    self.assertIsNotNone(message.binary_options_market_ids_to_cancel_all)

  async def test_cancel_orders(self):
    expected = MagicMock(spec=TxResponse)
    self.injective_chain._execute_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain.cancel_all_orders_for_markets(self.wallet, ["<market-id>"])

    self.assertEqual(expected, response)

    self.injective_chain._execute_transaction.assert_awaited_once()

    message = self.injective_chain._execute_transaction.call_args.args[1][0]

    self.assertIsNotNone(message.binary_options_orders_to_cancel)
