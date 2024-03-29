from datetime import datetime
from datetime import timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_positions import GetPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.get_positions import GetPositionsRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Subaccount
from frontrunner_sdk.models.wallet import Wallet


class TestGetPositionsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234", "0x5678"]
    self.subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.subaccount = Subaccount.from_subaccount_id(self.subaccount_id)
    self.positions = [MagicMock(), MagicMock()]

    self.position_response = MagicMock(
      positions=self.positions,
      paging=MagicMock(total=len(self.positions)),
    )

  def test_validate_market_ids_only(self):
    req = GetPositionsRequest(market_ids=self.market_ids)
    cmd = GetPositionsOperation(req)
    cmd.validate(self.deps)

  def test_validate_mine_only(self):
    req = GetPositionsRequest(mine=True)
    cmd = GetPositionsOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_mine_and_market_ids_missing(self):
    req = GetPositionsRequest()
    cmd = GetPositionsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_mutually_exclusive_params(self):
    with self.assertRaises(FrontrunnerArgumentException):
      GetPositionsOperation(GetPositionsRequest(subaccount=self.subaccount, subaccount_index=2)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      GetPositionsOperation(GetPositionsRequest(mine=True, subaccount=self.subaccount)).validate(self.deps)

  def test_validate_exception_when_start_in_future(self):
    start = datetime.now() + timedelta(days=1)
    req = GetPositionsRequest(market_ids=self.market_ids, mine=True, start_time=start)
    cmd = GetPositionsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_in_future(self):
    end = datetime.now() + timedelta(days=1)
    req = GetPositionsRequest(market_ids=self.market_ids, mine=True, end_time=end)
    cmd = GetPositionsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_before_start(self):
    ref = datetime.now()
    start = ref - timedelta(days=1)
    end = ref - timedelta(days=2)
    req = GetPositionsRequest(
      market_ids=self.market_ids,
      mine=True,
      start_time=start,
      end_time=end,
    )
    cmd = GetPositionsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  async def test_get_positions_market_ids(self):
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(market_ids=self.market_ids, mine=False)
    cmd = GetPositionsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.positions, self.positions)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once()

  async def test_get_positions_when_subaccount_index(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(subaccount_index=2)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      subaccount_id=self.wallet.subaccount_address(index=2),
    )

  async def test_get_positions_when_subaccount(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(subaccount=self.subaccount)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(subaccount_id=self.subaccount_id,)

  async def test_get_positions_when_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(market_ids=self.market_ids, mine=True)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_get_positions_when_subaccount_index_and_markets(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(market_ids=self.market_ids, subaccount_index=2)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_id=self.wallet.subaccount_address(index=2),
    )

  async def test_get_positions_when_subaccount_and_markets(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(market_ids=self.market_ids, subaccount=self.subaccount)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_id=self.subaccount_id,
    )

  async def test_get_positions_when_not_mine_and_subaccount(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(mine=False, subaccount=self.subaccount)
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(subaccount_id=self.subaccount_id,)

  async def test_get_positions_when_start_end_time(self):
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    ref = datetime.now()
    start = ref - timedelta(days=2)
    end = ref - timedelta(days=1)
    req = GetPositionsRequest(
      market_ids=self.market_ids,
      mine=False,
      start_time=start,
      end_time=end,
    )
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      start_time=int(start.timestamp()),
      end_time=int(end.timestamp()),
    )

  async def test_get_positions_when_direction_buy(self):
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="buy",
    )
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="long",
    )

  async def test_get_positions_when_direction_sell(self):
    self.deps.injective_client.get_derivative_positions = AsyncMock(return_value=self.position_response)

    req = GetPositionsRequest(
      market_ids=self.market_ids,
      mine=False,
      direction="sell",
    )
    cmd = GetPositionsOperation(req)
    await cmd.execute(self.deps)

    self.deps.injective_client.get_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      direction="short",
    )
