import itertools
import json

from dataclasses import dataclass
from dataclasses import field
from typing import List

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
    if not hasattr(injective_response, "tx_response"):
      return []

    tx_response = injective_response.tx_response

    if not hasattr(tx_response, "logs"):
      return []

    try:
      logs = list(tx_response.logs)
    except Exception:
      return []

    try:
      events = list(itertools.chain.from_iterable(log.events for log in logs))
    except Exception:
      return []

    return [
      clz(
        next((json.loads(attribute.value) for attribute in event.attributes if attribute.key == "flags"), []),
        next((json.loads(attribute.value) for attribute in event.attributes if attribute.key == "hashes"), []),
      ) for event in events if event.type == clz.EVENT_ORDER_FAIL_TYPE
    ]


@dataclass
class GetTransactionRequest:
  transaction_hash: str


@dataclass
class GetTransactionResponse:
  injective_response: GetTxResponse
  order_failures: List[OrderFailure] = field(default_factory=list)


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
