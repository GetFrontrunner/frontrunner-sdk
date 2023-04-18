import dataclasses
from dataclasses import dataclass
from typing import Any, List
from typing import AsyncIterator
from typing import Dict
from typing import Literal
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder, DerivativeOrderHistory  # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class StreamOrdersRequest:
  # internal fields
  mine: bool
  # passthrough fields
  market_id: str
  direction: Optional[Literal["buy", "sell"]] = None
  subaccount_id: Optional[str] = None
  order_types: Optional[List[str]] = None
  state: Optional[str] = None
  execution_types: Optional[List[str]] = None


@dataclass
class StreamOrdersResponse:
  orders: AsyncIterator[DerivativeOrderHistory]


class StreamOrdersOperation(FrontrunnerOperation[StreamOrdersRequest, StreamOrdersResponse]):

  def __init__(self, request: StreamOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_id:
      raise FrontrunnerArgumentException("'market_id' is required")

    if self.request.mine and self.request.subaccount_id:
      raise FrontrunnerArgumentException("'mine' and 'subaccount_id' are mutually exclusive")

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamOrdersResponse:
    request: Dict[str, Any] = dataclasses.asdict(self.request)
    request.pop("mine", None)

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()

    orders: AsyncIterator[DerivativeOrderHistory] = await injective_stream(
      deps.injective_client.stream_historical_derivative_orders,
      "order",
      **request,
    )
    return StreamOrdersResponse(orders)
