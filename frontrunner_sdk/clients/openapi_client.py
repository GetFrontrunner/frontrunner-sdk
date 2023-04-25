import functools
import logging

from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Mapping
from typing import Tuple
from typing import Type
from typing import TypeVar

from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException

OpenAPI = TypeVar("OpenAPI")
Result = TypeVar("Result")


def api_methods(api: Type[OpenAPI]):
  for name in dir(api):
    if name.startswith("__"):
      continue

    if name.endswith("with_http_info"):
      continue

    if not hasattr(api, f"{name}_with_http_info"):
      continue

    method_with_http_info = getattr(api, f"{name}_with_http_info")

    yield (name, method_with_http_info)


def with_exception(
  method: Callable[..., Awaitable[Tuple[Any, int, Mapping[str, str]]]]
) -> Callable[..., Awaitable[Tuple[Any, int, Mapping[str, str]]]]:

  @functools.wraps(method)
  async def wrapped(*args, **kwargs) -> Tuple[Any, int, Mapping[str, str]]:
    try:
      (result, status, headers) = await method(*args, **kwargs)

    except Exception as cause:
      raise FrontrunnerUnserviceableException("OpenAPI Framework Exception") from cause

    if status >= 500:
      raise FrontrunnerUnserviceableException("Service Exception", status=status, result=result)

    if status >= 400:
      raise FrontrunnerArgumentException("Client Exception", status=status, result=result)

    return (result, status, headers)

  wrapped.__wrapped__ = method # type: ignore

  return wrapped


def with_response_only(
  method: Callable[..., Awaitable[Tuple[Any, int, Mapping[str, str]]]],
) -> Callable[..., Awaitable[Any]]:

  @functools.wraps(method)
  async def wrapped(*args, **kwargs) -> Tuple[Any]:
    (response, _, _) = await method(*args, **kwargs)
    return response

  wrapped.__wrapped__ = method # type: ignore

  return wrapped


def with_debug_logging(
  api: object,
  method: Callable[..., Awaitable[Result]],
) -> Callable[..., Awaitable[Result]]:
  logger = logging.getLogger(api.__class__.__module__)

  @functools.wraps(method)
  async def wrapped(*args, **kwargs) -> Result:
    logger.debug(
      "Calling OpenAPI[%s] to %s with %s %s",
      api.__class__.__name__,
      method.__name__,
      str(args),
      str(kwargs),
    )

    result = await method(*args, **kwargs)

    logger.debug(
      "Received response from OpenAPI[%s] %s with %s %s",
      api.__class__.__name__,
      method.__name__,
      str(args),
      str(kwargs),
    )

    return result

  wrapped.__wrapped__ = method # type: ignore

  return wrapped


def openapi_client(api_type: Type[OpenAPI], *args, **kwargs) -> OpenAPI:

  # There's no good way around dynamic base types. Just ask mypy to overlook.
  # https://stackoverflow.com/a/59636248
  class OpenAPIClientWrapper(api_type): # type: ignore

    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

  for (name, method_with_http_info) in api_methods(api_type):
    replacement = method_with_http_info
    replacement = with_exception(replacement)
    replacement = with_debug_logging(api_type, replacement)
    replacement = with_response_only(replacement)

    setattr(OpenAPIClientWrapper, name, replacement)

  return OpenAPIClientWrapper(*args, **kwargs)
