from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api import MarketStatus
from frontrunner_sdk.openapi.frontrunner_api.models.market import Market


@dataclass
class GetMarketsRequest:
  id: Optional[str] = None
  injective_id: Optional[str] = None
  prop_id: Optional[str] = None
  event_id: Optional[str] = None
  league_id: Optional[str] = None
  status: Optional[MarketStatus] = None


@dataclass
class GetMarketsResponse:
  markets: Iterable[Market]


class GetMarketsOperation(FrontrunnerOperation[GetMarketsRequest, GetMarketsResponse]):

  def __init__(self, request: GetMarketsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetMarketsResponse:
    request = self.request_as_kwargs()
    markets = await deps.openapi_frontrunner_api.get_markets(**request)

    return GetMarketsResponse(markets=markets,)
