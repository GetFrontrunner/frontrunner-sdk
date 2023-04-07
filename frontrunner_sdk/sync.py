import asyncio

from typing import Any
from typing import Awaitable
from typing import Callable
from typing import TypeVar

Response = TypeVar("Response")


class SyncMixin:

  @staticmethod
  def _synchronously(
    operation: Callable[..., Awaitable[Response]],
    *args: Any,
    **kwargs: Any,
  ) -> Response:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(operation(*args, **kwargs))
