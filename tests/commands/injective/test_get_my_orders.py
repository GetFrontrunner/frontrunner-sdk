from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_my_orders import GetMyOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.get_my_orders import GetMyOrdersRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestGetMyOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.orders = [MagicMock(), MagicMock()]

    self.orders_response = MagicMock(
      orders=self.orders,
      paging=MagicMock(total=len(self.orders)),
    )

  def test_validate(self):
    req = GetMyOrdersRequest()
    cmd = GetMyOrdersOperation(req)
    cmd.validate(self.deps)

  async def test_get_orders(self):
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.deps.injective_client.get_derivative_subaccount_orders = AsyncMock(return_value=self.orders_response)

    req = GetMyOrdersRequest()
    cmd = GetMyOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.orders, self.orders)

    self.deps.injective_client.get_derivative_subaccount_orders.assert_awaited_once()
