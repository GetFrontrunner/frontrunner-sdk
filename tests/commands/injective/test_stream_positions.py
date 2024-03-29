from typing import Iterable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.stream_positions import StreamPositionsOperation # NOQA
from frontrunner_sdk.commands.injective.stream_positions import StreamPositionsRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Subaccount
from frontrunner_sdk.models.wallet import Wallet


class TestIterator:

  def __init__(self, items: Iterable):
    self.items = items

  async def response(self):
    for item in self.items:
      yield item


class TestStreamPositionsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234"]
    self.subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.subaccount = Subaccount.from_subaccount_id(self.subaccount_id)
    self.subaccount_ids = [self.subaccount_id, self.subaccount_id]
    self.subaccounts = [self.subaccount, self.subaccount]
    self.fake_position_contents = ["id1", "id2"]
    self.positions = [
      MagicMock(positions=self.fake_position_contents[0]),
      MagicMock(positions=self.fake_position_contents[1])
    ]
    self.positions_iterator = TestIterator(self.positions)
    self.positions_response = AsyncMock(return_value=self.positions_iterator.response())

  def test_validate(self):
    req = StreamPositionsRequest(market_ids=self.market_ids, mine=True)
    cmd = StreamPositionsOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_mine_and_subaccount_ids(self):
    req = StreamPositionsRequest(mine=True, subaccount_ids=self.subaccount_ids)
    cmd = StreamPositionsOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_mutually_exclusive_params(self):
    with self.assertRaises(FrontrunnerArgumentException):
      StreamPositionsOperation(StreamPositionsRequest(mine=True,
                                                      subaccount_ids=self.subaccount_ids)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamPositionsOperation(StreamPositionsRequest(mine=True, subaccounts=self.subaccounts)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamPositionsOperation(
        StreamPositionsRequest(mine=False, subaccounts=self.subaccounts, subaccount_ids=self.subaccount_ids)
      ).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamPositionsOperation(
        StreamPositionsRequest(mine=False, subaccount_ids=self.subaccount_ids, subaccount_indexes=[1, 2])
      ).validate(self.deps)

  async def test_stream_positions(self):
    self.deps.injective_client.stream_derivative_positions = self.positions_response

    req = StreamPositionsRequest(market_ids=self.market_ids, mine=False)
    cmd = StreamPositionsOperation(req)
    res = await cmd.execute(self.deps)

    # note that it is necessary to evaluate the response iterator (here we do it with list comprehension)
    # in position for the assert_awaited_* calls to succeed
    self.assertEqual(self.positions, [t async for t in res.positions])

    self.deps.injective_client.stream_derivative_positions.assert_awaited_once()

  async def test_stream_positions_when_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_derivative_positions = self.positions_response

    req = StreamPositionsRequest(market_ids=self.market_ids, mine=True)
    cmd = StreamPositionsOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.positions, [t async for t in res.positions])

    self.deps.injective_client.stream_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_ids=[self.wallet.subaccount_address()],
    )

  async def test_stream_positions_when_subaccount_indexes(self):
    subaccount_indexes = [1, 2]
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_derivative_positions = self.positions_response

    req = StreamPositionsRequest(market_ids=self.market_ids, mine=False, subaccount_indexes=subaccount_indexes)
    cmd = StreamPositionsOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.positions, [t async for t in res.positions])

    self.deps.injective_client.stream_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_ids=[self.wallet.subaccount_address(index) for index in subaccount_indexes],
    )

  async def test_stream_positions_when_subaccounts(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_derivative_positions = self.positions_response

    req = StreamPositionsRequest(market_ids=self.market_ids, mine=False, subaccounts=self.subaccounts)
    cmd = StreamPositionsOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.positions, [t async for t in res.positions])

    self.deps.injective_client.stream_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids,
      subaccount_ids=self.subaccount_ids,
    )

  async def test_stream_positions_when_other_fields(self):
    self.deps.injective_client.stream_derivative_positions = self.positions_response

    req = StreamPositionsRequest(
      market_ids=self.market_ids,
      subaccount_ids=self.subaccount_ids,
      mine=False,
    )
    cmd = StreamPositionsOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(self.positions, [t async for t in res.positions])

    self.deps.injective_client.stream_derivative_positions.assert_awaited_once_with(
      market_ids=self.market_ids, subaccount_ids=self.subaccount_ids
    )
