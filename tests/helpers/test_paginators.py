from typing import Any
from typing import Callable
from typing import Iterable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.helpers.paginators import injective_paginated_iterator
from frontrunner_sdk.helpers.paginators import injective_paginated_list


class TestInjectivePaginator(IsolatedAsyncioTestCase):

  @staticmethod
  def _paged_call(field: str, pages: Iterable[Iterable[Any]]) -> Callable[..., Any]:
    total = sum(len(page) for page in pages)

    return AsyncMock(side_effect=[MagicMock(
      paging=MagicMock(total=total),
      **{field: page},
    ) for page in pages])

  async def test_iterator_one_page(self):
    iterator = injective_paginated_iterator(
      self._paged_call("items", [
        [1, 2, 3],
      ]),
      "items",
    )

    self.assertEqual(
      [item async for item in iterator],
      [1, 2, 3],
    )

  async def test_iterator_multiple_pages(self):
    iterator = injective_paginated_iterator(
      self._paged_call("numbers", [
        [1, 2, 3],
        [4, 5],
      ]),
      "numbers",
    )

    self.assertEqual(
      [item async for item in iterator],
      [1, 2, 3, 4, 5],
    )

  async def test_iterator_empty_pages(self):
    iterator = injective_paginated_iterator(
      self._paged_call("numbers", [
        [1, 2],
        list(),
        [3, 4, 5],
      ]),
      "numbers",
    )

    self.assertEqual(
      [item async for item in iterator],
      [1, 2, 3, 4, 5],
    )

  async def test_paginated_list(self):
    result = await injective_paginated_list(
      self._paged_call("numbers", [
        ["my", "name"],
        ["is", "earl"],
      ]),
      "numbers",
    )

    self.assertEqual(result, ["my", "name", "is", "earl"])
