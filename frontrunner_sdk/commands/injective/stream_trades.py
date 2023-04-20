from dataclasses import dataclass
from typing import Any
from typing import AsyncIterator
from typing import Dict
from typing import Iterable
from typing import Literal
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeTrade # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class StreamTradesRequest:
  market_ids: Iterable[str]
  mine: bool
  direction: Optional[Literal["buy", "sell"]] = None
  side: Optional[Literal["maker", "taker"]] = None


@dataclass
class StreamTradesResponse:
  trades: AsyncIterator[DerivativeTrade]


class StreamTradesOperation(FrontrunnerOperation[StreamTradesRequest, StreamTradesResponse]):

  def __init__(self, request: StreamTradesRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_ids:
      raise FrontrunnerArgumentException("At least one market id is required")

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamTradesResponse:
    request: Dict[str, Any] = {
      "market_ids": list(self.request.market_ids),
    }

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()

    if self.request.direction:
      request["direction"] = self.request.direction

    if self.request.side:
      request["execution_side"] = self.request.side

    trades: AsyncIterator[DerivativeTrade] = await injective_stream(
      deps.injective_client.stream_derivative_trades,
      **request,
    )
    return StreamTradesResponse(trades)
