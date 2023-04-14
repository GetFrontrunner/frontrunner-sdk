from datetime import datetime
from datetime import timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_trades import GetTradesOperation # NOQA
from frontrunner_sdk.commands.injective.get_trades import GetTradesRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestGetTradesOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234", "0x5678"]
    self.trades = [MagicMock(), MagicMock()]

    self.trades_response = MagicMock(
      trades=self.trades,
      paging=MagicMock(total=len(self.trades)),
    )

  def test_validate(self):
    req = GetTradesRequest(market_ids=self.market_ids, mine=True)
    cmd = GetTradesOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_no_market_ids(self):
    req = GetTradesRequest(market_ids=[], mine=True)
    cmd = GetTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_start_in_future(self):
    start = datetime.now() + timedelta(days=1)
    req = GetTradesRequest(market_ids=self.market_ids, mine=True, start_time=start)
    cmd = GetTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_in_future(self):
    end = datetime.now() + timedelta(days=1)
    req = GetTradesRequest(market_ids=self.market_ids, mine=True, end_time=end)
    cmd = GetTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_before_start(self):
    ref = datetime.now()
    start = ref - timedelta(days=1)
    end = ref - timedelta(days=2)
    req = GetTradesRequest(
      market_ids=self.market_ids,
      mine=True,
      start_time=start,
      end_time=end,
    )
    cmd = GetTradesOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  async def test_get_trades(self):
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    req = GetTradesRequest(market_ids=self.market_ids, mine=False)
    cmd = GetTradesOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.trades, self.trades)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once()

  async def test_get_trades_when_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    req = GetTradesRequest(market_ids=self.market_ids, mine=True)
    cmd = GetTradesOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_get_trades_when_start_end_time(self):
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    ref = datetime.now()
    start = ref - timedelta(days=2)
    end = ref - timedelta(days=1)
    req = GetTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      start_time=start,
      end_time=end,
    )
    cmd = GetTradesOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      start_time=int(start.timestamp()),
      end_time=int(end.timestamp()),
    )

  async def test_get_trades_when_direction_buy(self):
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    req = GetTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="buy",
    )
    cmd = GetTradesOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="long",
    )

  async def test_get_trades_when_direction_sell(self):
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    req = GetTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="sell",
    )
    cmd = GetTradesOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="short",
    )

  async def test_get_trades_when_side(self):
    self.deps.injective_client.get_derivative_trades = AsyncMock(return_value=self.trades_response)

    req = GetTradesRequest(
      market_ids=self.market_ids,
      mine=False,
      side="maker",
    )
    cmd = GetTradesOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_trades.assert_awaited_once_with(
      market_ids=self.market_ids,
      execution_side="maker",
    )