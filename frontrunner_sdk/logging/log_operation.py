import functools
import logging

from typing import Awaitable
from typing import Callable
from typing import TypeVar

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC

Operation = TypeVar("Operation", bound=FrontrunnerOperation)
Response = TypeVar("Response")


def log_operation(module_name: str):
  logger = logging.getLogger(module_name)

  def logged_operation(operation: Callable[[Operation, FrontrunnerIoC], Awaitable[Response]]):

    @functools.wraps(operation)
    async def wrapped(instance: Operation, deps: FrontrunnerIoC) -> Response:
      value = await operation(instance, deps)
      logger.info("%s with %s", instance.__class__.__name__, instance.request)
      logger.debug("%s yielded %s", instance.request, value)
      return value

    return wrapped

  return logged_operation
