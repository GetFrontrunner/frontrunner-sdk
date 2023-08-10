from google.protobuf.message import Message

from frontrunner_sdk.clients.gas_estimators.gas_estimator import GasEstimator
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException


class TableGasEstimator(GasEstimator):
  # rates were derived experimentally, on testnet

  MESSAGE_RATES = {
    "MsgDeposit": 73532,
    "MsgWithdraw": 71077,
    "MsgExternalTransfer": 64769,
    "MsgSubaccountTransfer": 63789,
    "MsgBatchUpdateOrders": 50656,
  }

  ORDER_RATES = {
    "OrderData": 4878,
    "DerivativeOrder": 12884,
  }

  async def gas_for(self, message: Message) -> int:
    message_type = message.__class__.__name__

    if message_type not in self.MESSAGE_RATES:
      raise FrontrunnerInjectiveException(
        "Fee not available for message type",
        message_type=message_type,
      )

    gas = self.MESSAGE_RATES[message_type]

    if message_type.startswith("MsgBatch"):

      for descriptor, value in message.ListFields():
        if not descriptor.message_type:
          continue

        order_type = descriptor.message_type.name

        if order_type not in self.ORDER_RATES:
          raise FrontrunnerInjectiveException(
            "Fee not available for order type",
            message_type=message_type,
            order_type=descriptor.message_type.name,
          )

        gas += len(value) * self.ORDER_RATES[order_type]

    return gas
