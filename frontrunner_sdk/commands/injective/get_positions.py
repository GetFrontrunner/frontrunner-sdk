from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Literal
from typing import Optional
from typing import Sequence

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativePosition # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.paginators import injective_paginated_list
from frontrunner_sdk.helpers.validation import validate_start_time_end_time
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetPositionsRequest:
  mine: bool = False
  market_ids: Optional[Iterable[str]] = None
  direction: Optional[Literal["buy", "sell"]] = None
  start_time: Optional[datetime] = None
  end_time: Optional[datetime] = None


@dataclass
class GetPositionsResponse:
  positions: Sequence[DerivativePosition]


class GetPositionsOperation(FrontrunnerOperation[GetPositionsRequest, GetPositionsResponse]):

  def __init__(self, request: GetPositionsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.mine and not self.request.market_ids:
      raise FrontrunnerArgumentException("Either mine must be True, or at least one market id must be provided")

    validate_start_time_end_time(self.request.start_time, self.request.end_time)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetPositionsResponse:
    request: Dict[str, Any] = {}

    if self.request.mine:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address()

    if self.request.market_ids:
      request["market_ids"] = list(self.request.market_ids)

    if self.request.start_time:
      request["start_time"] = int(self.request.start_time.timestamp())

    if self.request.end_time:
      request["end_time"] = int(self.request.end_time.timestamp())

    if self.request.direction == "buy":
      request["direction"] = "long"
    elif self.request.direction == "sell":
      request["direction"] = "short"

    positions: Sequence[DerivativePosition] = await injective_paginated_list(
      deps.injective_client.get_derivative_positions,
      "positions",
      **request,
    )

    return GetPositionsResponse(positions=positions)
