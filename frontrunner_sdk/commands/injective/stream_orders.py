from dataclasses import dataclass
from typing import AsyncIterator
from typing import List
from typing import Literal
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder # NOQA
from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeOrderHistory # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.helpers.validation import validate_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import InjectiveOrderExecutionType
from frontrunner_sdk.models import InjectiveOrderState
from frontrunner_sdk.models import InjectiveOrderType
from frontrunner_sdk.models import OrderHistory


@dataclass
class StreamOrdersRequest:
  # internal fields
  mine: bool
  # passthrough fields
  market_id: str
  direction: Optional[Literal["buy", "sell"]] = None
  subaccount_id: Optional[str] = None
  order_types: Optional[List[InjectiveOrderType]] = None
  state: Optional[InjectiveOrderState] = None
  execution_types: Optional[List[InjectiveOrderExecutionType]] = None


@dataclass
class StreamOrdersResponse:
  orders: AsyncIterator[OrderHistory]


class StreamOrdersOperation(FrontrunnerOperation[StreamOrdersRequest, StreamOrdersResponse]):

  def __init__(self, request: StreamOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_id:
      raise FrontrunnerArgumentException("'market_id' is required")

    validate_mutually_exclusive("mine", self.request.mine, "subaccount_id", self.request.subaccount_id)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamOrdersResponse:
    request = self.request_as_kwargs()
    request.pop("mine", None)

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()

    injective_orders: AsyncIterator[DerivativeOrderHistory] = await injective_stream(
      deps.injective_client.stream_historical_derivative_orders,
      **request,
    )
    orders: AsyncIterator[OrderHistory] = OrderHistory._from_async_iterator(injective_orders)
    return StreamOrdersResponse(orders)
