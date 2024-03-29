from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.create_orders import CreateOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.create_orders import CreateOrdersRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order


class TestCreateOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.orders = [
      Order.buy_long("<market-id>", 10, 0.75),
      Order.buy_short("<market-id>", 10, 0.25, subaccount_index=1),
      Order.buy_short("<market-id2>", 10, 0.25, is_post_only=True),
    ]

  def test_validate(self):
    req = CreateOrdersRequest(orders=self.orders)
    cmd = CreateOrdersOperation(req)
    cmd.validate(self.deps)

  def test_validate_empty_orders_exception(self):
    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[])).validate(self.deps)

  def test_validate_order_quantity_invalid_exception(self):
    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[Order.buy_long("<market-id>", -2, 0.75)])).validate(self.deps)

  def test_validate_order_price_invalid_exception(self):
    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[Order.buy_long("<market-id>", 1, -0.25)])).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[Order.buy_long("<market-id>", 1, 0)])).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[Order.buy_long("<market-id>", 1, 1)])).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(CreateOrdersRequest(orders=[Order.buy_long("<market-id>", 1, 1.25)])).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      CreateOrdersOperation(
        CreateOrdersRequest(orders=[
          Order.buy_long("<market-id>", 1, 1.25),
          Order.buy_short("<market-id>", 1, 1.25),
        ])
      ).validate(self.deps)

  async def test_create_orders(self):
    self.deps.injective_chain.create_orders = AsyncMock(
      return_value=(
        MagicMock(txhash="<txhash>"),
        ["<hash-1>", "<hash-2>", "<hash-3>"],
      )
    )

    req = CreateOrdersRequest(orders=self.orders)
    cmd = CreateOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")
    self.assertEqual(
      [order.hash for order in res.orders],
      ["<hash-1>", "<hash-2>", "<hash-3>"],
    )

    self.deps.injective_chain.create_orders.assert_awaited_once_with(await self.deps.wallet(), self.orders)
