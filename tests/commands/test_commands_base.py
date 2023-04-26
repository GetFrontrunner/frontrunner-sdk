from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC


@dataclass
class FakeRequest:
  a: int
  b: str
  c: bool


@dataclass
class FakeResponse:
  result: str


class FakeOperation(FrontrunnerOperation[FakeRequest, FakeResponse]):

  def __init__(self, request: FakeRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  async def execute(self, deps: FrontrunnerIoC) -> FakeResponse:
    return None


class TestFrontrunnerOperation(IsolatedAsyncioTestCase):

  def test_request_as_kwargs(self):
    req = FakeRequest(a=0, b="hello", c=False)
    cmd = FakeOperation(req)

    kwargs = cmd.request_as_kwargs()

    self.assertEqual(kwargs, {"a": 0, "b": "hello", "c": False})
