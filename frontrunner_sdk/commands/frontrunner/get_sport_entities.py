from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api import SportEntity


@dataclass
class GetSportEntitiesRequest:
  id: Optional[str] = None
  league_id: Optional[str] = None
  sport: Optional[str] = None


@dataclass
class GetSportEntitiesResponse:
  sport_entities: Iterable[SportEntity]


class GetSportEntitiesOperation(FrontrunnerOperation[GetSportEntitiesRequest, GetSportEntitiesResponse]):

  def __init__(self, request: GetSportEntitiesRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetSportEntitiesResponse:
    request = self.request_as_kwargs()
    sport_entities = await deps.openapi_frontrunner_api.get_sport_entities(**request)

    return GetSportEntitiesResponse(sport_entities=sport_entities,)
