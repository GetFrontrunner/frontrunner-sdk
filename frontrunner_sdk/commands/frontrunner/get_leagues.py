from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api import League


@dataclass
class GetLeaguesRequest:
  id: Optional[str] = None
  sport: Optional[str] = None


@dataclass
class GetLeaguesResponse:
  leagues: Iterable[League]


class GetLeaguesOperation(FrontrunnerOperation[GetLeaguesRequest, GetLeaguesResponse]):

  def __init__(self, request: GetLeaguesRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetLeaguesResponse:
    request = self.request_as_kwargs()
    leagues = await deps.openapi_frontrunner_api.get_leagues(**request)

    return GetLeaguesResponse(leagues=leagues,)
