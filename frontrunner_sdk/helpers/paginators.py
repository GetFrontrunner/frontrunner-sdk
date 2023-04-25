import sys

from typing import Any
from typing import AsyncIterator
from typing import Awaitable
from typing import Callable
from typing import Iterable
from typing import Protocol
from typing import Sequence
from typing import TypeVar

Item = TypeVar("Item")


class InjectivePage(Protocol):
  total: int


class InjectivePaginatedResponse(Protocol):
  paging: InjectivePage


async def injective_paginated_iterator(
  call: Callable[..., Awaitable[InjectivePaginatedResponse]],
  field: str,
  *call_args: Any,
  **call_kwargs: Any,
) -> AsyncIterator[Item]:
  seen = 0
  total = sys.maxsize

  while seen < total:
    skip_kwargs = {"skip": seen} if seen > 0 else {}

    response = await call(*call_args, **call_kwargs, **skip_kwargs)

    total = response.paging.total
    items: Iterable[Item] = getattr(response, field)

    for item in items:
      seen += 1
      yield item


async def injective_paginated_list(
  call: Callable[..., Awaitable[InjectivePaginatedResponse]],
  field: str,
  *call_args: Any,
  **call_kwargs: Any,
) -> Sequence[Item]:
  paginated: AsyncIterator[Item] = injective_paginated_iterator(call, field, *call_args, **call_kwargs)
  return [item async for item in paginated]
