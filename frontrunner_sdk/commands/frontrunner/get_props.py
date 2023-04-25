from dataclasses import dataclass
from typing import Iterable
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.openapi.frontrunner_api import Prop


@dataclass
class GetPropsRequest:
  id: Optional[str] = None
  league_id: Optional[str] = None


@dataclass
class GetPropsResponse:
  props: Iterable[Prop]


class GetPropsOperation(FrontrunnerOperation[GetPropsRequest, GetPropsResponse]):

  def __init__(self, request: GetPropsRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetPropsResponse:
    request = self.request_as_kwargs()
    props = await deps.openapi_frontrunner_api.get_props(**request)

    return GetPropsResponse(props=props,)
