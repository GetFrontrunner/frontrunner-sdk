from typing import Callable
from typing import TypeVar

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC

Request = TypeVar("Request")
Response = TypeVar("Response")
OperationConstructor = Callable[[Request], FrontrunnerOperation[Request, Response]]


class FrontrunnerFacadeMixin:

  @staticmethod
  async def _run_operation(constructor: OperationConstructor, deps: FrontrunnerIoC, request: Request) -> Response:
    operation = constructor(request)
    operation.validate(deps)
    return await operation.execute(deps)
