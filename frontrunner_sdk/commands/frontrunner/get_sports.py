from dataclasses import dataclass
from typing import Iterable

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetSportsRequest:
  pass


@dataclass
class GetSportsResponse:
  sports: Iterable[str]


class GetSportsOperation(FrontrunnerOperation[GetSportsRequest, GetSportsResponse]):

  def __init__(self, request: GetSportsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetSportsResponse:
    request = self.request_as_kwargs()
    leagues = await deps.openapi_frontrunner_api.get_leagues(**request)
    sports = {league.sport for league in leagues}

    return GetSportsResponse(sports=sports,)
