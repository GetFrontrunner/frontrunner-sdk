import dataclasses

from dataclasses import dataclass
from typing import Any
from typing import AsyncIterator
from typing import Dict
from typing import Iterable
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativePosition # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.parameters import ignore_none
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class StreamPositionsRequest:
  # internal fields
  mine: bool
  # passthrough fields
  market_id: Optional[str]
  market_ids: Optional[Iterable[str]]
  subaccount_id: Optional[str]
  subaccount_ids: Optional[Iterable[str]]


@dataclass
class StreamPositionsResponse:
  positions: AsyncIterator[DerivativePosition]


class StreamPositionsOperation(FrontrunnerOperation[StreamPositionsRequest, StreamPositionsResponse]):

  def __init__(self, request: StreamPositionsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if (self.request.mine and self.request.subaccount_id) or (self.request.mine and self.request.subaccount_ids):
      raise FrontrunnerArgumentException(
        "'mine' and 'subaccount_id'/'subaccount_ids' are mutually exclusive",
        mine=self.request.mine,
        subaccount_id=self.request.subaccount_id,
        subaccount_ids=self.request.subaccount_ids,
      )

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamPositionsResponse:
    request: Dict[str, Any] = dataclasses.asdict(self.request, dict_factory=ignore_none)
    request.pop("mine", None)

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()

    positions: AsyncIterator[DerivativePosition] = await injective_stream(
      deps.injective_client.stream_derivative_positions,
      **request,
    )
    return StreamPositionsResponse(positions)
