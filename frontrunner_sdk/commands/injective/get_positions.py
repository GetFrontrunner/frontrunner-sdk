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
from frontrunner_sdk.helpers.validation import validate_start_time_end_time, validate_mutually_exclusive, validate_all_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class GetPositionsRequest:
  mine: bool = False
  subaccount: Optional[Subaccount] = None
  subaccount_index: Optional[int] = None
  market_ids: Optional[Iterable[str]] = None
  direction: Optional[Literal["buy", "sell"]] = None
  start_time: Optional[datetime] = None
  end_time: Optional[datetime] = None


@dataclass
class GetPositionsResponse:
  positions: Sequence[DerivativePosition]


class GetPositionsOperation(FrontrunnerOperation[GetPositionsRequest, GetPositionsResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccount", "subaccount_index"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount"]

  def __init__(self, request: GetPositionsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.mine and not self.request.market_ids:
      raise FrontrunnerArgumentException("Either mine must be True, or at least one market id must be provided")

    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE)
    validate_start_time_end_time(self.request.start_time, self.request.end_time)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetPositionsResponse:
    request: Dict[str, Any] = {}

    if self.request.mine or self.request.subaccount_index is not None:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address(self.request.subaccount_index or 0)

    if self.request.subaccount:
      request["subaccount_id"] = self.request.subaccount.subaccount_id

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
