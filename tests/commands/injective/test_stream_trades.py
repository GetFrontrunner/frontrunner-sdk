from datetime import datetime
from datetime import timedelta
from typing import Iterable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.stream_trades import StreamTradesOperation # NOQA
from frontrunner_sdk.commands.injective.stream_trades import StreamTradesRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestIterator:

  def __init__(self, items: Iterable):
    self.items = items

  async def response(self):
    for item in self.items:
      yield item


class TestStreamTradesOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234", "0x5678"]
    self.fake_trade_contents = ["id1", "id2"]
    self.trades = [MagicMock(trade=self.fake_trade_contents[0]), MagicMock(trade=self.fake_trade_contents[1])]
    self.trades_iterator = TestIterator(self.trades)
    self.trades_response = AsyncMock(return_value=self.trades_iterator.response())

  def test_validate(self):
    req = StreamTradesRequest(market_ids=self.market_ids, mine=True)
    cmd = StreamTradesOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_no_market_ids(self):
    req = StreamTradesRequest(market_ids=[], mine=True)
    cmd = StreamTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_start_in_future(self):
    start = datetime.now() + timedelta(days=1)
    req = StreamTradesRequest(market_ids=self.market_ids, mine=True, start_time=start)
    cmd = StreamTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_in_future(self):
    end = datetime.now() + timedelta(days=1)
    req = StreamTradesRequest(market_ids=self.market_ids, mine=True, end_time=end)
    cmd = StreamTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_before_start(self):
    ref = datetime.now()
    start = ref - timedelta(days=1)
    end = ref - timedelta(days=2)
    req = StreamTradesRequest(
      market_ids=self.market_ids,
      mine=True,
      start_time=start,
      end_time=end,
    )
    cmd = StreamTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  async def test_stream_trades(self):
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    req = StreamTradesRequest(market_ids=self.market_ids, mine=False)
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)

    # note that it is necessary to evaluate the response iterator (here we do it with list comprehension)
    # in order for the assert_awaited_* calls to succeed
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once()

  async def test_stream_trades_when_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    req = StreamTradesRequest(market_ids=self.market_ids, mine=True)
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_stream_trades_when_start_end_time(self):
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    ref = datetime.now()
    start = ref - timedelta(days=2)
    end = ref - timedelta(days=1)
    req = StreamTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      start_time=start,
      end_time=end,
    )
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      start_time=int(start.timestamp()),
      end_time=int(end.timestamp()),
    )

  async def test_stream_trades_when_direction_buy(self):
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    req = StreamTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="buy",
    )
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="long",
    )

  async def test_stream_trades_when_direction_sell(self):
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    req = StreamTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="sell",
    )
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="short",
    )

  async def test_stream_trades_when_side(self):
    self.deps.injective_client.stream_derivative_trades = self.trades_response

    req = StreamTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      side="maker",
    )
    cmd = StreamTradesOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.fake_trade_contents, [t async for t in res.trades])

    self.deps.injective_client.stream_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      execution_side="maker",
    )