from google.protobuf.message import Message

from frontrunner_sdk.clients.gas_estimators.table_gas_estimator import TableGasEstimator # NOQA


class MultiplierTableGasEstimator(TableGasEstimator):
  # Multiply per-message type gas estimates by the configured value

  def __init__(self, multiplier: int):
    self.multiplier = multiplier

  async def gas_for(self, message: Message) -> int:
    base_gas = await super().gas_for(message)

    return base_gas * self.multiplier
