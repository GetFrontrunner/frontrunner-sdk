import asyncio
import logging
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


class MockOperation(FrontrunnerOperation[str, str]):

  def __init__(self, request: str):
    self.request = request

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> str:
    await asyncio.sleep(1)
    return "response"


class TestLogOperation(IsolatedAsyncioTestCase):

  async def test_log_operation(self):
    deps = MagicMock(spec=FrontrunnerIoC)
    operation = MockOperation("request")

    with self.assertLogs() as logs:
      await operation.execute(deps)

      record = logs.records[0]

      self.assertEqual(record.name, __name__)
      self.assertEqual(record.levelno, logging.INFO)
      self.assertEqual(record.message, "MockOperation with request, yielding response")
