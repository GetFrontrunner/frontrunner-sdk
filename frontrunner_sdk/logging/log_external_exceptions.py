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

  # Ideally, we don't use `...` as the parameter specification becaues if the
  # caller to the underlying function messes up the types, there's no way to
  # detect it. Params are basically treated as `Any`. There's a PEP that
  # introduces support for parameter types. However, it's for Python 3.10+, and
  # we're supporting 3.8+, so we can't "use" it.
  #
  # If we _could_ use it, this would be typed as:
  #
  #   Params = ParamSpec("Params")
  #   def decorator(callable: Callable[Params, Awaitable[Result]]) -> Callable[Params, Awaitable[Result]]:
  #     # ...
  #
  # https://stackoverflow.com/a/47060298
  # https://peps.python.org/pep-0612/
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
