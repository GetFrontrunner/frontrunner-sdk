from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin
from frontrunner_sdk.ioc import FrontrunnerIoC


class MockOperation(FrontrunnerOperation[str, str]):

  def __init__(self, request: str):
    self.request = request

  def validate(self, deps: FrontrunnerIoC) -> None:
    print("called")

  async def execute(self, deps: FrontrunnerIoC) -> str:
    return "response"


class MockFacade(FrontrunnerFacadeMixin):

  async def do_something(self, request: str) -> str:
    return await self._run_operation(MockOperation, MagicMock(spec=FrontrunnerIoC), request)


class TestFrontrunnerFacadeMixin(IsolatedAsyncioTestCase):

  async def test_run_operation(self):
    with patch.object(MockOperation, "validate") as _validate:
      with patch.object(MockOperation, "execute") as _execute:
        facade = MockFacade()

        await facade.do_something("request")

        _validate.assert_called_once()
        _execute.assert_awaited_once()
