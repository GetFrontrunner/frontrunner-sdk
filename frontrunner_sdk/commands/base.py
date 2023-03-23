from abc import ABC
from abc import abstractmethod
from typing import Generic
from typing import TypeVar

from frontrunner_sdk.ioc import FrontrunnerIoC

Response = TypeVar("Response")
Request = TypeVar("Request")


class FrontrunnerOperation(Generic[Request, Response], ABC):

  def __init__(self, request: Request):
    self.request = request

  @abstractmethod
  async def execute(self, deps: FrontrunnerIoC) -> Response:
    pass
