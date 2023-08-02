from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeTrade # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.paginators import injective_paginated_list
from frontrunner_sdk.helpers.validation import validate_all_mutually_exclusive
from frontrunner_sdk.helpers.validation import validate_start_time_end_time
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class GetTradesRequest:
  market_ids: Iterable[str]
  mine: bool
  subaccount: Optional[Subaccount] = None
  subaccount_index: Optional[int] = None
  subaccounts: Optional[List[Subaccount]] = None
  subaccount_indexes: Optional[List[int]] = None
  direction: Optional[Literal["buy", "sell"]] = None
  side: Optional[Literal["maker", "taker"]] = None
  start_time: Optional[datetime] = None
  end_time: Optional[datetime] = None


@dataclass
class GetTradesResponse:
  trades: Sequence[DerivativeTrade]


class GetTradesOperation(FrontrunnerOperation[GetTradesRequest, GetTradesResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccount", "subaccount_index", "subaccounts", "subaccount_indexes"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE_PLURAL = ["mine", "subaccounts"]

  def __init__(self, request: GetTradesRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_ids:
      raise FrontrunnerArgumentException("At least one market id is required")

    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE_PLURAL)
    validate_start_time_end_time(self.request.start_time, self.request.end_time)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetTradesResponse:
    request: Dict[str, Any] = {
      "market_ids": list(self.request.market_ids),
    }

    if (self.request.mine and not self.request.subaccount_indexes) or self.request.subaccount_index is not None:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address(self.request.subaccount_index or 0)

    elif self.request.subaccount:
      request["subaccount_id"] = self.request.subaccount.subaccount_id

    elif self.request.subaccount_indexes:
      wallet = await deps.wallet()
      request["subaccount_ids"] = [wallet.subaccount_address(index) for index in self.request.subaccount_indexes]

    elif self.request.subaccounts:
      request["subaccount_ids"] = [subaccount.subaccount_id for subaccount in self.request.subaccounts]

    if self.request.start_time:
      request["start_time"] = int(self.request.start_time.timestamp())

    if self.request.end_time:
      request["end_time"] = int(self.request.end_time.timestamp())

    if self.request.direction:
      request["direction"] = self.request.direction

    if self.request.side:
      request["execution_side"] = self.request.side

    trades: Sequence[DerivativeTrade] = await injective_paginated_list(
      deps.injective_client.get_derivative_trades,
      "trades",
      **request,
    )

    return GetTradesResponse(trades=trades)
