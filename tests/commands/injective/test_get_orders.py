from datetime import datetime
from datetime import timedelta
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_orders import GetOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.get_orders import GetOrdersRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models import OrderHistory
from frontrunner_sdk.models.wallet import Wallet


class TestGetOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = ["0x1234"]
    self.order_types = ["stop_buy"]
    self.execution_types = ["limit"]
    self.orders = [MagicMock(direction="buy", is_reduce_only=False), MagicMock(direction="buy", is_reduce_only=False)]

    self.orders_response = MagicMock(
      orders=self.orders,
      paging=MagicMock(total=len(self.orders)),
    )

  def test_validate(self):
    req = GetOrdersRequest(mine=True)
    cmd = GetOrdersOperation(req)
    cmd.validate(self.deps)

  def test_validate_exception_when_mine_and_subaccount_id(self):
    req = GetOrdersRequest(mine=True, subaccount_id="1234")
    cmd = GetOrdersOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_start_in_future(self):
    start = datetime.now() + timedelta(days=1)
    req = GetOrdersRequest(market_ids=self.market_ids, mine=True, start_time=start)
    cmd = GetOrdersOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_in_future(self):
    end = datetime.now() + timedelta(days=1)
    req = GetOrdersRequest(market_ids=self.market_ids, mine=True, end_time=end)
    cmd = GetOrdersOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  def test_validate_exception_when_end_before_start(self):
    ref = datetime.now()
    start = ref - timedelta(days=1)
    end = ref - timedelta(days=2)
    req = GetOrdersRequest(
      market_ids=self.market_ids,
      mine=True,
      start_time=start,
      end_time=end,
    )
    cmd = GetOrdersOperation(req)

    with self.assertRaises(FrontrunnerArgumentException):
      cmd.validate(self.deps)

  async def test_get_orders_mine(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_historical_derivative_orders = AsyncMock(return_value=self.orders_response)

    req = GetOrdersRequest(mine=True)
    cmd = GetOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.orders, OrderHistory._from_injective_derivative_order_histories(self.orders))

    self.deps.injective_client.get_historical_derivative_orders.assert_awaited_once_with(
      None,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_get_orders_not_mine_and_subaccount(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_historical_derivative_orders = AsyncMock(return_value=self.orders_response)

    req = GetOrdersRequest(mine=False, subaccount=self.wallet.subaccount())
    cmd = GetOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.orders, OrderHistory._from_injective_derivative_order_histories(self.orders))

    self.deps.injective_client.get_historical_derivative_orders.assert_awaited_once_with(
      None,
      subaccount_id=self.wallet.subaccount_address(),
    )

  async def test_get_orders_other_args(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_historical_derivative_orders = AsyncMock(return_value=self.orders_response)
    ref = datetime.now()
    start = ref - timedelta(days=2)
    end = ref - timedelta(days=1)
    req = GetOrdersRequest(
      mine=False,
      subaccount_id="1234",
      market_ids=self.market_ids,
      direction="buy",
      is_conditional=False,
      order_types=self.order_types,
      execution_types=self.execution_types,
      state="booked",
      start_time=start,
      end_time=end
    )
    cmd = GetOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.orders, OrderHistory._from_injective_derivative_order_histories(self.orders))

    self.deps.injective_client.get_historical_derivative_orders.assert_awaited_once_with(
      None,
      subaccount_id="1234",
      market_ids=self.market_ids,
      direction="buy",
      is_conditional="false",
      order_types=self.order_types,
      execution_types=self.execution_types,
      state="booked",
      start_time=int(start.timestamp()),
      end_time=int(end.timestamp()),
    )
