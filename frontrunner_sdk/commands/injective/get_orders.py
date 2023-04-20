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
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetOrdersRequest:
  # internal fields
  mine: bool
  # passthrough fields
  market_ids: Optional[List[str]] = None
  subaccount_id: Optional[str] = None
  direction: Optional[Literal["buy", "sell"]] = None
  is_conditional: Optional[bool] = None
  order_types: Optional[List[str]] = None
  state: Optional[str] = None
  execution_types: Optional[List[str]] = None
  start_time: Optional[datetime] = None
  end_time: Optional[datetime] = None


@dataclass
class GetOrdersResponse:
  orders: Sequence[DerivativeOrderHistory]


class GetOrdersOperation(FrontrunnerOperation[GetOrdersRequest, GetOrdersResponse]):

  def __init__(self, request: GetOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    now = datetime.now()

    if self.request.mine and self.request.subaccount_id:
      raise FrontrunnerArgumentException(
        "'mine' and 'subaccount_id' are mutually exclusive",
        mine=self.request.mine,
        subaccount_id=self.request.subaccount_id
      )

    if self.request.start_time and self.request.start_time > now:
      raise FrontrunnerArgumentException(
        "Start time cannot be in the future",
        now=now,
        start_time=self.request.start_time,
      )

    if self.request.end_time and self.request.end_time > now:
      raise FrontrunnerArgumentException(
        "End time cannot be in the future",
        now=now,
        end_time=self.request.end_time,
      )

    if self.request.start_time and self.request.end_time and self.request.start_time > self.request.end_time:
      raise FrontrunnerArgumentException(
        "Start time cannot be after end time",
        start_time=self.request.start_time,
        end_time=self.request.end_time,
      )

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetOrdersResponse:
    request = self.request_as_kwargs()
    request.pop("mine", None)

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()
    if self.request.is_conditional is not None:
      request["is_conditional"] = str(self.request.is_conditional).lower()

    if self.request.start_time:
      request["start_time"] = int(self.request.start_time.timestamp())

    if self.request.end_time:
      request["end_time"] = int(self.request.end_time.timestamp())

    orders: Sequence[DerivativeLimitOrder] = await injective_paginated_list(
      deps.injective_client.get_historical_derivative_orders,
      "orders",
      # Force market_id=None since we use optional market_ids param instead
      # TODO: remove workaround once Injective SDK has market_id as optional
      None,
      **request,
    )

    return GetOrdersResponse(orders=orders)