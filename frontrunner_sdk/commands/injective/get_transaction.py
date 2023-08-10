import json

from collections import Iterable
from dataclasses import dataclass
from typing import List
from typing import Optional

from pyinjective.proto.cosmos.tx.v1beta1.service_pb2 import GetTxResponse

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class OrderFailure:
  flags: List[int]
  hashes: List[str]

  EVENT_ORDER_FAIL_TYPE = "injective.exchange.v1beta1.EventOrderFail"

  @classmethod
  def from_injective_response(clz, injective_response: GetTxResponse) -> list:
    result = []
    if getattr(injective_response, "tx_response"):
      tx_response = injective_response.tx_response
      if getattr(tx_response, "logs"):
        logs = tx_response.logs
        if logs and issubclass(type(logs), Iterable):
          for log in logs:
            for event in log.events:
              if event.type == clz.EVENT_ORDER_FAIL_TYPE:
                attributes = event.attributes
                flags: List[int] = next(
                  (json.loads(attribute.value) for attribute in attributes if attribute.key == "flags"), []
                )
                hashes: List[str] = next(
                  (json.loads(attribute.value) for attribute in attributes if attribute.key == "hashes"), []
                )
                result.append(clz(flags, hashes))

    return result


@dataclass
class GetTransactionRequest:
  transaction_hash: str


@dataclass
class GetTransactionResponse:
  injective_response: GetTxResponse
  order_failures: List[OrderFailure] = None


class GetTransactionOperation(FrontrunnerOperation[GetTransactionRequest, GetTransactionResponse]):

  def __init__(self, request: GetTransactionRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetTransactionResponse:
    response = await deps.injective_client.get_tx(self.request.transaction_hash)
    order_failures = OrderFailure.from_injective_response(response)
    return GetTransactionResponse(injective_response=response, order_failures=order_failures)
