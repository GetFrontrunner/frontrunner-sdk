import itertools
import json

from dataclasses import dataclass
from dataclasses import field
from typing import Iterable
from typing import List

from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import Attribute
from pyinjective.proto.cosmos.base.abci.v1beta1.abci_pb2 import StringEvent
from pyinjective.proto.cosmos.tx.v1beta1.service_pb2 import GetTxResponse

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.helpers.encoders import b64_to_hex
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class OrderFailure:
  flags: List[int]
  hashes: List[str]

  EVENT_ORDER_FAIL_TYPE = "injective.exchange.v1beta1.EventOrderFail"

  @classmethod
  def _flags(clz, attributes: Iterable[Attribute]) -> List[int]:
    flags = itertools.chain.from_iterable(
      json.loads(attribute.value) for attribute in attributes if attribute.key == "flags"
    )

    return list(flags)

  @classmethod
  def _hashes(clz, attributes: Iterable[Attribute]) -> List[str]:
    raw_hashes = itertools.chain.from_iterable(
      json.loads(attribute.value) for attribute in attributes if attribute.key == "hashes"
    )

    return list("0x" + b64_to_hex(raw_hash) for raw_hash in raw_hashes)

  @classmethod
  def _from_event(clz, event: StringEvent) -> "OrderFailure":
    return clz(
      clz._flags(event.attributes),
      clz._hashes(event.attributes),
    )

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

    return [clz._from_event(event) for event in events if event.type == clz.EVENT_ORDER_FAIL_TYPE]


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
