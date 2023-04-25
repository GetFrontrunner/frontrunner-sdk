from dataclasses import dataclass
from datetime import datetime
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api import SportEvent


@dataclass
class GetSportEventsRequest:
  id: Optional[str] = None
  league_id: Optional[str] = None
  sport: Optional[str] = None
  starts_since: Optional[datetime] = None


@dataclass
class GetSportEventsResponse:
  sport_events: Iterable[SportEvent]


class GetSportEventsOperation(FrontrunnerOperation[GetSportEventsRequest, GetSportEventsResponse]):

  def __init__(self, request: GetSportEventsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetSportEventsResponse:
    request = self.request_as_kwargs()
    sport_events = await deps.openapi_frontrunner_api.get_sport_events(**request)

    return GetSportEventsResponse(sport_events=sport_events,)
