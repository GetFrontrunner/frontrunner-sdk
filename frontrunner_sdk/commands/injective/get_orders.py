from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder # NOQA
from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeOrderHistory # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.paginators import injective_paginated_list
from frontrunner_sdk.helpers.validation import validate_all_mutually_exclusive
from frontrunner_sdk.helpers.validation import validate_start_time_end_time
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import InjectiveOrderExecutionType
from frontrunner_sdk.models import InjectiveOrderState
from frontrunner_sdk.models import InjectiveOrderType
from frontrunner_sdk.models import OrderHistory
from frontrunner_sdk.models import Subaccount


@dataclass
class GetOrdersRequest:
  # internal fields
  mine: Optional[bool] = None
  # passthrough fields
  market_ids: Optional[List[str]] = None
  subaccount_id: Optional[str] = None
  subaccount: Optional[Subaccount] = None
  subaccount_index: Optional[int] = None
  direction: Optional[Literal["buy", "sell"]] = None
  is_conditional: Optional[bool] = None
  order_types: Optional[List[InjectiveOrderType]] = None
  state: Optional[InjectiveOrderState] = None
  execution_types: Optional[List[InjectiveOrderExecutionType]] = None
  start_time: Optional[datetime] = None
  end_time: Optional[datetime] = None


@dataclass
class GetOrdersResponse:
  orders: Sequence[OrderHistory]


class GetOrdersOperation(FrontrunnerOperation[GetOrdersRequest, GetOrdersResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccount_id", "subaccount", "subaccount_index"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount_id", "subaccount"]

  def __init__(self, request: GetOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    if self.request.mine and self.request.subaccount or self.request.mine and self.request.subaccount_id:
      raise FrontrunnerArgumentException(
        "mine and subaccount[_id] are mutually exclusive",
        mine=self.request.mine,
        subaccount=self.request.subaccount,
        subaccount_id=self.request.subaccount_id
      )
    validate_start_time_end_time(self.request.start_time, self.request.end_time)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetOrdersResponse:
    request = self.request_as_kwargs()
    request.pop("mine", None)
    request.pop("subaccount", None)
    request.pop("subaccount_index", None)

    if self.request.mine or self.request.subaccount_index is not None:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address(self.request.subaccount_index or 0)

    if self.request.subaccount:
      request["subaccount_id"] = self.request.subaccount.subaccount_id

    if self.request.is_conditional is not None:
      request["is_conditional"] = str(self.request.is_conditional).lower()

    if self.request.start_time:
      request["start_time"] = int(self.request.start_time.timestamp())

    if self.request.end_time:
      request["end_time"] = int(self.request.end_time.timestamp())

    injective_orders: Sequence[DerivativeOrderHistory] = await injective_paginated_list(
      deps.injective_client.get_historical_derivative_orders,
      "orders",
      # Force market_id=None since we use optional market_ids param instead
      # TODO: remove workaround once Injective SDK has market_id as optional
      None,
      **request,
    )

    orders = OrderHistory._from_injective_derivative_order_histories(injective_orders)

    return GetOrdersResponse(orders=orders)
