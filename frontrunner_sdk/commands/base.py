import dataclasses

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import Generic
from typing import TypeVar

from frontrunner_sdk.helpers.parameters import ignore_none
from frontrunner_sdk.ioc import FrontrunnerIoC

Response = TypeVar("Response")
Request = TypeVar("Request")


class FrontrunnerOperation(Generic[Request, Response], ABC):

  def __init__(self, request: Request):
    self.request = request
    request_data: Dict[str, Any] = dataclasses.asdict(self.request, dict_factory=ignore_none)
    request_data.pop("mine", None)
    self.request_data = request_data

  @abstractmethod
  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @abstractmethod
  async def execute(self, deps: FrontrunnerIoC) -> Response:
    pass
