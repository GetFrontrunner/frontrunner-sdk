from dataclasses import dataclass
from typing import AsyncIterator
from typing import Iterable

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeMarketInfo # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class StreamMarketsRequest:
  market_ids: Iterable[str]


@dataclass
class StreamMarketsResponse:
  markets: AsyncIterator[DerivativeMarketInfo]


class StreamMarketsOperation(FrontrunnerOperation[StreamMarketsRequest, StreamMarketsResponse]):

  def __init__(self, request: StreamMarketsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_ids:
      raise FrontrunnerArgumentException("market_ids is required")

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamMarketsResponse:
    request = self.request_as_kwargs()

    positions: AsyncIterator[DerivativeMarketInfo] = await injective_stream(
      deps.injective_client.stream_derivative_markets,
      **request,
    )
    return StreamMarketsResponse(positions)
