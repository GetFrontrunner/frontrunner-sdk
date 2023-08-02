from dataclasses import dataclass
from typing import AsyncIterator
from typing import Iterable
from typing import List
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativePosition # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.helpers.validation import validate_all_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class StreamPositionsRequest:
  # internal required fields
  mine: bool
  # passthrough required fields
  market_ids: Optional[Iterable[str]] = None
  subaccount_ids: Optional[Iterable[str]] = None
  # internal optional fields
  subaccounts: Optional[List[Subaccount]] = None
  subaccount_indexes: Optional[List[int]] = None


@dataclass
class StreamPositionsResponse:
  positions: AsyncIterator[DerivativePosition]


class StreamPositionsOperation(FrontrunnerOperation[StreamPositionsRequest, StreamPositionsResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccounts", "subaccount_indexes"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount_ids", "subaccounts"]

  def __init__(self, request: StreamPositionsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamPositionsResponse:
    request = self.request_as_kwargs()
    request.pop("mine", None)

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_ids"] = [wallet.subaccount_address()]

    if self.request.subaccount_indexes:
      wallet = await deps.wallet()
      request["subaccount_ids"] = [wallet.subaccount_address(index) for index in self.request.subaccount_indexes]

    if self.request.subaccounts:
      request["subaccount_ids"] = [subaccount.subaccount_id for subaccount in self.request.subaccounts]

    positions: AsyncIterator[DerivativePosition] = await injective_stream(
      deps.injective_client.stream_derivative_positions,
      **request,
    )
    return StreamPositionsResponse(positions)
