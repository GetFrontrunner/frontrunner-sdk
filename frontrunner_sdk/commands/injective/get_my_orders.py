from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Literal
from typing import Optional
from typing import Sequence

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrder # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.paginators import injective_paginated_list
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetMyOrdersRequest:
  pass


@dataclass
class GetMyOrdersResponse:
  orders: Sequence[DerivativeLimitOrder]


class GetMyOrdersOperation(FrontrunnerOperation[GetMyOrdersRequest, GetMyOrdersResponse]):

  def __init__(self, request: GetMyOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetMyOrdersResponse:
    wallet = await deps.wallet()

    orders: Sequence[DerivativeLimitOrder] = await injective_paginated_list(
      deps.injective_client.get_derivative_subaccount_orders,
      "orders",
      subaccount_id=wallet.subaccount_address(),
    )

    return GetMyOrdersResponse(orders=orders)
