from typing import Iterable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.stream_markets import StreamMarketsOperation # NOQA
from frontrunner_sdk.commands.injective.stream_markets import StreamMarketsRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestIterator:

  def __init__(self, items: Iterable):
    self.items = items

  async def response(self):
    for item in self.items:
      yield item


class TestStreamMarketsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234"]
    self.fake_market_contents = ["id1", "id2"]
    self.markets = [MagicMock(markets=self.fake_market_contents[0]), MagicMock(markets=self.fake_market_contents[1])]
    self.markets_iterator = TestIterator(self.markets)
    self.markets_response = AsyncMock(return_value=self.markets_iterator.response())

  def test_validate(self):
    req = StreamMarketsRequest(market_ids=self.market_ids)
    cmd = StreamMarketsOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_no_market_ids(self):
    req = StreamMarketsRequest(market_ids=[])
    cmd = StreamMarketsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  async def test_stream_markets(self):
    self.deps.injective_client.stream_derivative_markets = self.markets_response

    req = StreamMarketsRequest(market_ids=self.market_ids)
    cmd = StreamMarketsOperation(req)
    res = await cmd.execute(self.deps)

    # note that it is necessary to evaluate the response iterator (here we do it with list comprehension)
    # in order for the assert_awaited_* calls to succeed
    self.assertEqual(self.markets, [t async for t in res.markets])

    self.deps.injective_client.stream_derivative_markets.assert_awaited_once_with(market_ids=self.market_ids)
