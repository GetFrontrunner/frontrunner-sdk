from unittest import IsolatedAsyncioTestCase

from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgBatchUpdateOrders # NOQA
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgCreateSpotMarketOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgDeposit
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgRewardsOptOut # NOQA
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import OrderData

from frontrunner_sdk.clients.gas_estimators.table_gas_estimator import TableGasEstimator # NOQA
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException


class TestTableGasEstimator(IsolatedAsyncioTestCase):

  def setUp(self):
    self.estimator = TableGasEstimator()

  async def test_gas_for_unknown_message(self):
    msg = MsgRewardsOptOut()

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.estimator.gas_for(msg)

  async def test_gas_for_unknown_order(self):
    msg = MsgCreateSpotMarketOrder()

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.estimator.gas_for(msg)

  async def test_gas_for_non_composite_message(self):
    msg = MsgDeposit()

    self.assertEqual(
      TableGasEstimator.MESSAGE_RATES["MsgDeposit"],
      await self.estimator.gas_for(msg),
    )

  async def test_gas_for_composite_message(self):
    msg = MsgBatchUpdateOrders(
      binary_options_orders_to_create=[DerivativeOrder(), DerivativeOrder()],
      binary_options_orders_to_cancel=[OrderData()],
    )

    self.assertEqual(
      TableGasEstimator.MESSAGE_RATES["MsgBatchUpdateOrders"] + 2 * TableGasEstimator.ORDER_RATES["DerivativeOrder"] +
      1 * TableGasEstimator.ORDER_RATES["OrderData"],
      await self.estimator.gas_for(msg),
    )
