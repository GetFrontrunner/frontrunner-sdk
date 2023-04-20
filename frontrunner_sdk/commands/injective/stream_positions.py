from dataclasses import dataclass
from typing import AsyncIterator
from typing import Iterable
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativePosition # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class StreamPositionsRequest:
  # internal fields
  mine: bool
  # passthrough fields
  market_ids: Optional[Iterable[str]] = None
  subaccount_ids: Optional[Iterable[str]] = None


@dataclass
class StreamPositionsResponse:
  positions: AsyncIterator[DerivativePosition]


class StreamPositionsOperation(FrontrunnerOperation[StreamPositionsRequest, StreamPositionsResponse]):

  def __init__(self, request: StreamPositionsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if self.request.mine and self.request.subaccount_ids:
      raise FrontrunnerArgumentException(
        "'mine' and 'subaccount_ids' are mutually exclusive",
        mine=self.request.mine,
        subaccount_ids=self.request.subaccount_ids,
      )

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamPositionsResponse:
    if self.request.mine:
      wallet = await deps.wallet()
      self.request_data["subaccount_ids"] = [wallet.subaccount_address()]

    positions: AsyncIterator[DerivativePosition] = await injective_stream(
      deps.injective_client.stream_derivative_positions,
      **self.request_data,
    )
    return StreamPositionsResponse(positions)