import asyncio
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from unittest import TestCase
from unittest.mock import patch

from frontrunner_sdk.sync import SyncMixin


class TestSDK(SyncMixin):

  async def operation_async(
    self,
    arg: str,
    *args: int,
    kwarg: str = "",
    **kwargs: int,
  ) -> Tuple[List[Any], Dict[str, Any]]:
    await asyncio.sleep(1)
    return ([arg, *args], {"kwarg": kwarg, **kwargs})

  def operation_sync(self, arg: str, *args: int, kwarg: str = "", **kwargs):
    return self._synchronously(self.operation_async, arg, *args, kwarg=kwarg, **kwargs)


class TestSyncMixin(TestCase):

  def test_synchronously(self):
    sdk = TestSDK()

    with patch.object(TestSDK, "operation_async", wraps=sdk.operation_async) as _operation_async:
      positional, keywowrd = sdk.operation_sync("operation", 2, 3, 4, kwarg="keyword", a=0, z=25)

      _operation_async.assert_awaited_once_with("operation", 2, 3, 4, kwarg="keyword", a=0, z=25)

      self.assertEqual(positional, ["operation", 2, 3, 4])
      self.assertEqual(keywowrd, {"kwarg": "keyword", "a": 0, "z": 25})
