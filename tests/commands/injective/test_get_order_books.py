from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksOperation # NOQA
from frontrunner_sdk.commands.injective.get_order_books import GetOrderBooksRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestGetOrderBooksOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate(self):
    req = GetOrderBooksRequest(market_ids=[])
    cmd = GetOrderBooksOperation(req)
    cmd.validate(self.deps)

  async def test_execute(self):
    abc_orderbook = MagicMock()
    xyz_orderbook = MagicMock()

    response = MagicMock()
    response.orderbooks = [
      MagicMock(market_id="abc", orderbook=abc_orderbook),
      MagicMock(market_id="xyz", orderbook=xyz_orderbook),
    ]

    self.deps.injective_client.get_derivative_orderbooksV2 = AsyncMock(return_value=response)

    req = GetOrderBooksRequest(market_ids=["abc", "xyz"])
    cmd = GetOrderBooksOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIn("abc", res.order_books)
    self.assertIn("xyz", res.order_books)

    self.assertEqual(res.order_books["abc"], abc_orderbook)
    self.assertEqual(res.order_books["xyz"], xyz_orderbook)
