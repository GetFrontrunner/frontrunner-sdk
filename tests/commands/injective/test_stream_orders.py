from typing import Iterable
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.stream_orders import StreamOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.stream_orders import StreamOrdersRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models import OrderHistory
from frontrunner_sdk.models.wallet import Wallet, Subaccount


class TestIterator:

  def __init__(self, items: Iterable):
    self.items = items

  async def response(self):
    for item in self.items:
      yield item


class TestStreamOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_id = "0x1234"
    self.subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.subaccount = Subaccount.from_subaccount_id(self.subaccount_id)
    self.fake_order_contents = [
      MagicMock(direction="buy", is_reduce_only=False),
      MagicMock(direction="buy", is_reduce_only=False)
    ]
    self.orders = [MagicMock(order=o) for o in self.fake_order_contents]
    self.orders_iterator = TestIterator(self.orders)
    self.orders_response = AsyncMock(return_value=self.orders_iterator.response())

  def test_validate(self):
    req = StreamOrdersRequest(market_id=self.market_id, mine=True)
    cmd = StreamOrdersOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_no_market_id(self):
    req = StreamOrdersRequest(market_id="", mine=True)
    cmd = StreamOrdersOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_mutually_exclusive_params(self):
    with self.assertRaises(FrontrunnerArgumentException):
      StreamOrdersOperation(StreamOrdersRequest(market_id=self.market_id, mine=True, subaccount_id="1234")).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamOrdersOperation(StreamOrdersRequest(market_id=self.market_id, mine=False, subaccount=self.subaccount, subaccount_index=2)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamOrdersOperation(StreamOrdersRequest(market_id=self.market_id, mine=False, subaccount_id=self.subaccount_id, subaccount_index=2)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamOrdersOperation(StreamOrdersRequest(market_id=self.market_id, mine=False, subaccount_id=self.subaccount_id, subaccount=self.subaccount)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      StreamOrdersOperation(StreamOrdersRequest(market_id=self.market_id, mine=True, subaccount=self.subaccount)).validate(self.deps)

  async def test_stream_orders(self):
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(market_id=self.market_id, mine=False)
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)

    # note that it is necessary to evaluate the response iterator (here we do it with list comprehension)
    # in order for the assert_awaited_* calls to succeed
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once()

  async def test_stream_orders_when_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(market_id=self.market_id, mine=True)
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_stream_orders_when_index_and_not_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(market_id=self.market_id, mine=False, subaccount_index=2)
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id,
      subaccount_id=self.wallet.subaccount_address(index=2),
    )

  async def test_stream_orders_when_index_and_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(market_id=self.market_id, mine=True, subaccount_index=2)
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id,
      subaccount_id=self.wallet.subaccount_address(index=2),
    )

  async def test_stream_orders_when_subaccount(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(market_id=self.market_id, mine=False, subaccount=self.subaccount)
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id,
      subaccount_id=self.subaccount_id,
    )

  async def test_stream_orders_when_direction_sell(self):
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(
      market_id=self.market_id,
      mine=False,
      direction="sell",
    )
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id,
      direction="sell",
    )

  async def test_stream_orders_when_other_fields(self):
    self.deps.injective_client.stream_historical_derivative_orders = self.orders_response

    req = StreamOrdersRequest(
      market_id=self.market_id,
      mine=False,
      direction="buy",
      state="booked",
      order_types=["buy"],
      execution_types=["limit"]
    )
    cmd = StreamOrdersOperation(req)
    res = await cmd.execute(self.deps)
    self.assertEqual(
      OrderHistory._from_injective_derivative_order_histories(self.fake_order_contents), [t async for t in res.orders]
    )

    self.deps.injective_client.stream_historical_derivative_orders.assert_awaited_once_with(
      market_id=self.market_id, direction="buy", state="booked", order_types=["buy"], execution_types=["limit"]
    )
