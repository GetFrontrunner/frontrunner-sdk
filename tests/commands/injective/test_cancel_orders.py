from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersOperation # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet


class TestCancelOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.wallet = Wallet._new()
    self.market_ids = ["0x1234", "0x5678"]
    self.order_responses = [MagicMock(market_id=id) for id in self.market_ids]

  def test_validate(self):
    req = CancelOrdersRequest(wallet=self.wallet)
    cmd = CancelAllOrdersOperation(req)
    cmd.validate(self.deps)

  async def test_cancel_orders(self):
    self.deps.injective_chain.get_all_open_orders = AsyncMock(return_value=self.order_responses)
    self.deps.injective_chain.cancel_all_orders_for_markets = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = CancelOrdersRequest(wallet=self.wallet)
    cmd = CancelAllOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.get_all_open_orders.assert_awaited_once()
    self.deps.injective_chain.cancel_all_orders_for_markets.assert_awaited_once_with(self.wallet, self.market_ids)
