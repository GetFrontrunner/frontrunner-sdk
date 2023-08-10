from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from pyinjective.async_client import AsyncClient
from pyinjective.composer import Composer
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import GasInfo # NOQA
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import TxResponse # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderInfo
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderType
from pyinjective.transaction import Transaction
from pyinjective.utils.utils import derivative_price_to_backend
from pyinjective.utils.utils import derivative_quantity_to_backend

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator
from frontrunner_sdk.clients.injective_chain import InjectiveChain
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Subaccount
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

    self.subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.subaccount = Subaccount.from_subaccount_id(self.subaccount_id)

    self.client = MagicMock(spec=AsyncClient)
    self.network = MagicMock(spec=Network)
    self.composer = MagicMock(wraps=Composer(self.network))
    self.gas_estimator = MagicMock(spec=GasEstimator)
    self.injective_chain = InjectiveChain(self.composer, self.client, self.network, self.gas_estimator)

    self.network.fee_denom = "inj"
    self.network.chain_id = "<chain-id>"

  async def test_estimate_cost(self):
    self.gas_estimator.gas_for = AsyncMock(return_value=1000)

    gas, fee = await self.injective_chain._estimate_cost([self.order])

    self.assertEqual(gas, 1000)
    self.assertEqual(fee[0].amount, str(InjectiveChain.GAS_PRICE * 1000))

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

  async def test_send_transaction_success(self):
    expected = TxResponse(code=0)
    self.client.send_tx_sync_mode = AsyncMock(return_value=expected)

    response = await self.injective_chain._send_transaction(self.wallet, [self.order], 100, [])

    self.assertEqual(expected, response)
    self.assertEqual(1, self.wallet.sequence)

  async def test_send_transaction_failure(self):
    expected = TxResponse(code=7, raw_log="boom")
    self.client.send_tx_sync_mode = AsyncMock(return_value=expected)

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_chain._send_transaction(self.wallet, [self.order], 100, [])
      self.assertEqual(0, self.wallet.sequence)

  async def test_execute_transaction(self):
    expected = MagicMock(spec=TxResponse)

    self.injective_chain._estimate_cost = AsyncMock(return_value=(5, []))
    self.injective_chain._send_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain._execute_transaction(self.wallet, [self.order])

    self.assertEqual(expected, response)

    self.injective_chain._estimate_cost.assert_awaited_once()
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

    response = await self.injective_chain.cancel_all_orders_for_markets(self.wallet, self.subaccount, ["<market-id>"])

    self.assertEqual(expected, response)

    self.injective_chain._execute_transaction.assert_awaited_once()

    message = self.injective_chain._execute_transaction.call_args.args[1][0]

    self.assertIsNotNone(message.binary_options_market_ids_to_cancel_all)

  async def test_cancel_orders(self):
    expected = MagicMock(spec=TxResponse)
    self.injective_chain._execute_transaction = AsyncMock(return_value=expected)

    response = await self.injective_chain.cancel_all_orders_for_markets(self.wallet, self.subaccount, ["<market-id>"])

    self.assertEqual(expected, response)

    self.injective_chain._execute_transaction.assert_awaited_once()

    message = self.injective_chain._execute_transaction.call_args.args[1][0]

    self.assertIsNotNone(message.binary_options_orders_to_cancel)
