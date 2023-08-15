from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderInfo
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderType

from frontrunner_sdk.clients.injective_order_hasher import InjectiveOrderHasher
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveOrderHasher(IsolatedAsyncioTestCase):

  def setUp(self):
    self.wallet = Wallet._new()
    self.network = MagicMock(lcd_endpoint="http://lcd.endpoint")
    self.wallet_fn = AsyncMock(return_value=self.wallet)
    self.order_hasher = InjectiveOrderHasher(self.network, self.wallet_fn)

  @patch("requests.get", return_value=MagicMock(json=MagicMock(return_value={"nonce": 0})))
  def test_hasher_for(self, _get):
    hasher = self.order_hasher._hasher_for(self.wallet, 0)

    cached = self.order_hasher._hasher_for(self.wallet, 0)

    _get.assert_called_once_with(
      url="http://lcd.endpoint/injective/exchange/v1beta1/exchange/" + self.wallet.subaccount_address(0)
    )

    self.assertIs(hasher, cached)

  @patch("requests.get", return_value=MagicMock(json=MagicMock(return_value={"nonce": 0})))
  async def test_reset_all(self, _get):
    hasher = self.order_hasher._hasher_for(self.wallet, 0)

    await self.order_hasher.reset()

    cached = self.order_hasher._hasher_for(self.wallet, 0)

    _get.assert_has_calls([
      call(url="http://lcd.endpoint/injective/exchange/v1beta1/exchange/" + self.wallet.subaccount_address(0)),
      call(url="http://lcd.endpoint/injective/exchange/v1beta1/exchange/" + self.wallet.subaccount_address(0)),
    ])

    self.assertIsNot(hasher, cached)

  @patch("requests.get", return_value=MagicMock(json=MagicMock(return_value={"nonce": 0})))
  async def test_reset_one(self, _get):
    hasher = self.order_hasher._hasher_for(self.wallet, 0)
    other = self.order_hasher._hasher_for(self.wallet, 1)

    await self.order_hasher.reset(0)

    hasher_cached = self.order_hasher._hasher_for(self.wallet, 0)
    other_cached = self.order_hasher._hasher_for(self.wallet, 1)

    self.assertIsNot(hasher, hasher_cached)
    self.assertIs(other, other_cached)

  @patch("requests.get", return_value=MagicMock(json=MagicMock(return_value={"nonce": 0})))
  async def test_hash(self, _get):
    order = DerivativeOrder(
      market_id="<market-id>",
      order_info=OrderInfo(
        subaccount_id=self.wallet.subaccount_address(),
        fee_recipient=self.wallet.subaccount_address(),
        price="500000",
        quantity="100",
      ),
      margin="500000",
      order_type=OrderType.BUY,
      trigger_price="500000",
    )

    order_hash = await self.order_hasher.hash(order, 0)

    await self.order_hasher.reset()

    order_rehash = await self.order_hasher.hash(order, 0)

    self.assertEqual(order_hash, order_rehash)

    order_again = await self.order_hasher.hash(order, 0)

    self.assertNotEqual(order_hash, order_again)
