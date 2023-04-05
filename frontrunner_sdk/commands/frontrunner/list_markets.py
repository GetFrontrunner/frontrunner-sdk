from dataclasses import dataclass
from typing import Optional
from typing import Sequence

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api.models.market import Market
from frontrunner_sdk.openapi.frontrunner_api.models.market_status import MarketStatus # NOQA


@dataclass
class ListMarketsRequest:
  id: Optional[str] = None
  injective_id: Optional[str] = None
  prop_id: Optional[str] = None
  event_id: Optional[str] = None
  league_id: Optional[str] = None
  status: Optional[MarketStatus] = None


@dataclass
class ListMarketsResponse:
  markets: Sequence[Market]


class ListMarketsOperation(FrontrunnerOperation[ListMarketsRequest, ListMarketsResponse]):

  def __init__(self, request: ListMarketsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> ListMarketsResponse:
    response = await deps.openapi_frontrunner_api.get_markets()
    return ListMarketsResponse(markets=response)
