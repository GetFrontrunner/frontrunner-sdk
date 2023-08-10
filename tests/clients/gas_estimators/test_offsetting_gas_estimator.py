from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator
from frontrunner_sdk.clients.gas_estimators.offsetting_gas_estimator import OffsettingGasEstimator # NOQA


class TestTableGasEstimator(IsolatedAsyncioTestCase):

  def setUp(self):
    self.base_estimator = MagicMock(spec=GasEstimator)
    self.base_estimator.gas_for = AsyncMock(return_value=0)

    self.estimator = OffsettingGasEstimator(self.base_estimator)

  async def test_gas_for_unknown_message(self):
    self.base_estimator.gas_for.return_value = 10_000

    self.assertEqual(
      10_000 + OffsettingGasEstimator.GAS_OFFSET,
      await self.estimator.gas_for(MagicMock()),
    )
