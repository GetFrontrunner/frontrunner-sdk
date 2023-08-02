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
from frontrunner_sdk.helpers.validation import validate_all_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import InjectiveOrderExecutionType
from frontrunner_sdk.models import InjectiveOrderState
from frontrunner_sdk.models import InjectiveOrderType
from frontrunner_sdk.models import OrderHistory
from frontrunner_sdk.models import Subaccount


@dataclass
class StreamOrdersRequest:
  # internal required fields
  mine: bool
  # passthrough required fields
  market_id: str
  # internal fields
  subaccount: Optional[Subaccount] = None
  subaccount_index: Optional[int] = None
  # passthrough fields
  direction: Optional[Literal["buy", "sell"]] = None
  subaccount_id: Optional[str] = None
  order_types: Optional[List[InjectiveOrderType]] = None
  state: Optional[InjectiveOrderState] = None
  execution_types: Optional[List[InjectiveOrderExecutionType]] = None


@dataclass
class StreamOrdersResponse:
  orders: AsyncIterator[OrderHistory]


class StreamOrdersOperation(FrontrunnerOperation[StreamOrdersRequest, StreamOrdersResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccount_id", "subaccount", "subaccount_index"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount_id", "subaccount"]

  def __init__(self, request: StreamOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_id:
      raise FrontrunnerArgumentException("'market_id' is required")

    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamOrdersResponse:
    request = self.request_as_kwargs()
    request.pop("mine", None)
    request.pop("subaccount", None)
    request.pop("subaccount_index", None)

    if self.request.mine or self.request.subaccount_index is not None:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address(self.request.subaccount_index or 0)

    if self.request.subaccount:
      request["subaccount_id"] = self.request.subaccount.subaccount_id

    injective_orders: AsyncIterator[DerivativeOrderHistory] = await injective_stream(
      deps.injective_client.stream_historical_derivative_orders,
      **request,
    )
    orders: AsyncIterator[OrderHistory] = OrderHistory._from_async_iterator(injective_orders)
    return StreamOrdersResponse(orders)
