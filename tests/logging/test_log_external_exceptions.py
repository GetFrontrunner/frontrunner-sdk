import logging
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from frontrunner_sdk.exceptions import FrontrunnerExternalException

from frontrunner_sdk.logging.log_external_exceptions import log_external_exceptions


class TestExternalException(FrontrunnerExternalException):
  def __init__(self, message, **kwargs) -> None:
    super().__init__(message, **kwargs)


class TestLogExternalException(IsolatedAsyncioTestCase):

  async def test_log_on_external_exception(self):

    @log_external_exceptions(__name__)
    async def action():
      raise TestExternalException("boom")

    with self.assertLogs(level=logging.CRITICAL) as logs:
      with self.assertRaises(TestExternalException):
        await action()

      record = logs.records[0]

      self.assertEqual(record.name, __name__)
      self.assertEqual(record.levelno, logging.CRITICAL)
      self.assertEqual(record.message, "boom")

  async def test_no_log_on_other_exceptions(self):

    @log_external_exceptions(__name__)
    async def action():
      raise RuntimeError("boom")

    with patch.object(logging.Logger, "critical") as _critical:
      with self.assertRaises(RuntimeError):
        await action()

      _critical.assert_not_called()
