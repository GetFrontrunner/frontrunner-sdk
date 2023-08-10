from dataclasses import dataclass

from pyinjective.proto.cosmos.tx.v1beta1.service_pb2 import GetTxResponse

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetTransactionRequest:
  transaction_hash: str


@dataclass
class GetTransactionResponse:
  response: GetTxResponse


class GetTransactionOperation(FrontrunnerOperation[GetTransactionRequest, GetTransactionResponse]):

  def __init__(self, request: GetTransactionRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetTransactionResponse:
    # for now, this is a straight proxy call, and we return the raw result;
    # return may be augmented in the future.
    response = await deps.injective_client.get_tx(self.request.transaction_hash)

    return GetTransactionResponse(response=response)
