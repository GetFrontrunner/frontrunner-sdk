import functools
import logging
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

from frontrunner_sdk.exceptions import FrontrunnerExternalException

Result = TypeVar("Result")


def log_external_exceptions(module_name: str):
  logger = logging.getLogger(module_name)

  def logged_callable(callable: Callable[..., Awaitable[Result]]):

    @functools.wraps(callable)
    async def wrapped(*args: Any, **kwargs: Any) -> Result:
      try:
        return await callable(*args, **kwargs)

      except FrontrunnerExternalException as exception:
        logger.critical(exception)
        raise exception

    return wrapped

  return logged_callable
