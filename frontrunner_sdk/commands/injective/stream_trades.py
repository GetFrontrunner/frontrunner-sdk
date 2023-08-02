from dataclasses import dataclass
from typing import Any
from typing import AsyncIterator
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Optional

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeTrade # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.streams import injective_stream
from frontrunner_sdk.helpers.validation import validate_all_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class StreamTradesRequest:
  market_ids: Iterable[str]
  mine: bool
  direction: Optional[Literal["buy", "sell"]] = None
  side: Optional[Literal["maker", "taker"]] = None
  # internal fields
  subaccount: Optional[Subaccount] = None
  subaccount_index: Optional[int] = None
  subaccounts: Optional[List[Subaccount]] = None
  subaccount_indexes: Optional[List[int]] = None


@dataclass
class StreamTradesResponse:
  trades: AsyncIterator[DerivativeTrade]


class StreamTradesOperation(FrontrunnerOperation[StreamTradesRequest, StreamTradesResponse]):

  MUTUALLY_EXCLUSIVE_PARAMS = ["subaccount", "subaccount_index", "subaccounts", "subaccount_indexes"]
  MUTUALLY_EXCLUSIVE_PARAMS_MINE = ["mine", "subaccount_id", "subaccount"]

  def __init__(self, request: StreamTradesRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not self.request.market_ids:
      raise FrontrunnerArgumentException("At least one market id is required")

    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS)
    validate_all_mutually_exclusive(self.request, self.MUTUALLY_EXCLUSIVE_PARAMS_MINE)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> StreamTradesResponse:
    request: Dict[str, Any] = {
      "market_ids": list(self.request.market_ids),
    }

    if self.request.mine or self.request.subaccount_index is not None:
      wallet = await deps.wallet()
      request["subaccount_id"] = wallet.subaccount_address(self.request.subaccount_index or 0)

    if self.request.subaccount:
      request["subaccount_id"] = self.request.subaccount.subaccount_id

    if self.request.subaccount_indexes:
      wallet = await deps.wallet()
      request["subaccount_ids"] = [wallet.subaccount_address(index) for index in self.request.subaccount_indexes]

    if self.request.subaccounts:
      request["subaccount_ids"] = [subaccount.subaccount_id for subaccount in self.request.subaccounts]

    if self.request.direction:
      request["direction"] = self.request.direction

    if self.request.side:
      request["execution_side"] = self.request.side

    trades: AsyncIterator[DerivativeTrade] = await injective_stream(
      deps.injective_client.stream_derivative_trades,
      **request,
    )
    return StreamTradesResponse(trades)
