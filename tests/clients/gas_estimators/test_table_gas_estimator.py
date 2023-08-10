from unittest import IsolatedAsyncioTestCase
from google.protobuf.message import Message

from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgRewardsOptOut
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgBatchUpdateOrders
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgCreateSpotMarketOrder
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import SpotOrder
from frontrunner_sdk.clients.gas_estimators.table_gas_estimator import TableGasEstimator
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException


class TestTableGasEstimator(IsolatedAsyncioTestCase):

  def setUp(self):
    self.estimator = TableGasEstimator()

  async def test_gas_for_unknown_message(self):
    msg = MsgRewardsOptOut(sender="sender")

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.estimator.gas_for(msg)

  async def test_gas_for_unknown_order(self):
    msg = MsgCreateSpotMarketOrder(
      sender="<wallet-address>",
      order=SpotOrder(),
    )

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.estimator.gas_for(msg)
