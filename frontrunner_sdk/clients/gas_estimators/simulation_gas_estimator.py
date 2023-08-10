import logging

from typing import Awaitable
from typing import Callable
from typing import cast

from google.protobuf.message import Message
from grpc.aio import AioRpcError
from pyinjective.async_client import AsyncClient
from pyinjective.constant import Network
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import SimulationResponse # NOQA
from pyinjective.transaction import Transaction

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.models.wallet import Wallet

logger = logging.getLogger(__name__)


class SimulationGasEstimator(GasEstimator):

  GAS_OFFSET = 20_000

  def __init__(self, client: AsyncClient, network: Network, walletFn: Callable[[], Awaitable[Wallet]]):
    self.client = client
    self.network = network
    self.walletFn = walletFn

  async def gas_for(self, message: Message) -> int:
    wallet = await self.walletFn()

    transaction = Transaction(
      msgs=[message],
      sequence=wallet.sequence,
      account_num=wallet.account_number,
      chain_id=self.network.chain_id,
    )

    signed = wallet.sign(wallet, transaction)

    logger.debug(
      "Calling Injective chain to simulate transaction with message=%s account=%s sequence=%s chain_id=%s",
      str(message),
      wallet.account_number,
      wallet.sequence,
      self.network.chain_id,
    )

    result, success = await self.client.simulate_tx(signed)

    if not success:
      cause = cast(AioRpcError, result)
      raise FrontrunnerInjectiveException(
        "Simulation failed",
        code=cause.code(),
        message=cause.debug_error_string(),
        details=cause.details(),
      )

    response = cast(SimulationResponse, result)

    logger.debug("Received simulation response from Injective chain yielding response=%s", response)

    return response.gas_info.gas_used
