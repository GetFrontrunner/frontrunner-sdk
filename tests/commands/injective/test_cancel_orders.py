from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelAllOrdersRequest # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersOperation # NOQA
from frontrunner_sdk.commands.injective.cancel_orders import CancelOrdersRequest # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.cancel_order import CancelOrder
from frontrunner_sdk.models.wallet import Subaccount
from frontrunner_sdk.models.wallet import Wallet


class TestCancelOrdersOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.market_ids = {"0x1234", "0x5678"}
    self.order_responses = [MagicMock(market_id=id) for id in self.market_ids]
    self.orders_cancel = [CancelOrder(market_id="<market-id>", order_hash="<order-hash>")]

  def test_validate_cancel_all_orders(self):
    req = CancelAllOrdersRequest()
    cmd = CancelAllOrdersOperation(req)
    cmd.validate(self.deps)

  def test_validate_cancel_orders(self):
    req = CancelOrdersRequest(self.orders_cancel)
    cmd = CancelOrdersOperation(req)
    cmd.validate(self.deps)

  async def test_cancel_all_orders(self):
    wallet = Wallet._new()
    subaccount = Subaccount.from_wallet_and_index(wallet, 0)

    self.deps.wallet = AsyncMock(return_value=wallet)
    self.deps.injective_chain.get_all_open_orders = AsyncMock(return_value=self.order_responses)
    self.deps.injective_chain.cancel_all_orders_for_markets = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = CancelAllOrdersRequest()
    cmd = CancelAllOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")
    self.assertEqual(res.orders, self.order_responses)

    self.deps.injective_chain.get_all_open_orders.assert_awaited_once()
    self.deps.injective_chain.cancel_all_orders_for_markets.assert_awaited_once_with(
      wallet, subaccount, self.market_ids
    )

  async def test_cancel_all_orders_subaccount_index(self):
    subaccount_index = 2
    wallet = Wallet._new()
    subaccount = Subaccount.from_wallet_and_index(wallet, subaccount_index)

    self.deps.wallet = AsyncMock(return_value=wallet)
    self.deps.injective_chain.get_all_open_orders = AsyncMock(return_value=self.order_responses)
    self.deps.injective_chain.cancel_all_orders_for_markets = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = CancelAllOrdersRequest(subaccount_index=subaccount_index)
    cmd = CancelAllOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")
    self.assertEqual(res.orders, self.order_responses)

    self.deps.injective_chain.get_all_open_orders.assert_awaited_once()
    self.deps.injective_chain.cancel_all_orders_for_markets.assert_awaited_once_with(
      wallet, subaccount, self.market_ids
    )

  async def test_cancel_all_orders_when_no_orders(self):
    wallet = Wallet._new()

    self.deps.wallet = AsyncMock(return_value=wallet)
    self.deps.injective_chain.get_all_open_orders = AsyncMock(return_value=[])
    self.deps.injective_chain.cancel_all_orders_for_markets = AsyncMock()

    req = CancelAllOrdersRequest()
    cmd = CancelAllOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertIsNone(res.transaction)
    self.assertEqual(res.orders, [])

    self.deps.injective_chain.cancel_all_orders_for_markets.assert_not_awaited()

  async def test_cancel_orders(self):
    wallet = Wallet._new()

    self.deps.wallet = AsyncMock(return_value=wallet)
    self.deps.injective_chain.cancel_orders = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = CancelOrdersRequest(orders=self.orders_cancel)
    cmd = CancelOrdersOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.cancel_orders.assert_awaited_once_with(wallet, self.orders_cancel)
