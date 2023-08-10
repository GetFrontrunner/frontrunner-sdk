from typing import Tuple
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from grpc import StatusCode
from grpc.aio import AioRpcError
from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import GasInfo
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import SimulationResponse # NOQA
from pyinjective.proto.injective.exchange.v1beta1.tx_pb2 import MsgDeposit

from frontrunner_sdk.clients.gas_estimators.simulation_gas_estimator import SimulationGasEstimator # NOQA
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.models.wallet import Wallet


class TestTableGasEstimator(IsolatedAsyncioTestCase):

  def setUp(self):
    self.client = MagicMock(spec=AsyncClient)
    self.client.simulate_tx = AsyncMock(return_value=(None, None))
    self.network = MagicMock(spec=Network, chain_id="<chain-id>")
    self.wallet = Wallet._new()
    self.estimator = SimulationGasEstimator(self.client, self.network, self.walletFn)

  async def walletFn(self) -> Wallet:
    return self.wallet

  def _simulation_response(self, gas: int) -> Tuple[SimulationResponse, bool]:
    return (
      SimulationResponse(gas_info=GasInfo(gas_used=gas)),
      True,
    )

  def _aio_rpc_error(self, code: StatusCode, details: str) -> Tuple[AioRpcError, bool]:
    return (
      AioRpcError(code, MagicMock(), MagicMock(), details=details),
      False,
    )

  async def test_gas_for_success(self):
    self.client.simulate_tx.return_value = self._simulation_response(10_000)

    msg = MsgDeposit()

    self.assertEqual(
      10_000,
      await self.estimator.gas_for(msg),
    )

  async def test_gas_for_failure(self):
    self.client.simulate_tx.return_value = self._aio_rpc_error(StatusCode.UNKNOWN, "boom")

    msg = MsgDeposit()

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.estimator.gas_for(msg)
