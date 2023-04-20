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

  def request_as_kwargs(self) -> Dict[str, Any]:
    return dataclasses.asdict(self.request, dict_factory=ignore_none) # type: ignore[call-overload]

  @abstractmethod
  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @abstractmethod
  async def execute(self, deps: FrontrunnerIoC) -> Response:
    pass
