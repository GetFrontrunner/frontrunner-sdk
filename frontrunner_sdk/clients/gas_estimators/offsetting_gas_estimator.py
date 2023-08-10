from google.protobuf.message import Message

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator


class OffsettingGasEstimator(GasEstimator):

  GAS_OFFSET = 20_000

  def __init__(self, estimator: GasEstimator):
    self.estimator = estimator

  async def gas_for(self, message: Message) -> int:
    return self.GAS_OFFSET + await self.estimator.gas_for(message)
