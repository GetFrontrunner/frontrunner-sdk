from unittest import TestCase

from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import OrderInfo
from pyinjective.transaction import Transaction

from frontrunner_sdk.models import Wallet


class TestWallet(TestCase):

  def setUp(self):
    self.wallet = Wallet._new()

  def test_identity(self):
    # these objects may modify themselves, so if they're regenerated, all
    # modifications are lost.
    self.assertIs(self.wallet.public_key, self.wallet.public_key)
    self.assertIs(self.wallet.address, self.wallet.address)

  def test_get_and_increment_sequence(self):
    self.wallet.address.sequence = 7

    self.assertEqual(7, self.wallet.sequence)

    old = self.wallet.get_and_increment_sequence()

    self.assertEqual(7, old)
    self.assertEqual(8, self.wallet.sequence)

  def test_sign(self):
    transaction = Transaction(
      msgs=[
        DerivativeOrder(
          trigger_price="0",
          margin="4500000",
          market_id="<market-id>",
          order_type="BUY",
          order_info=OrderInfo(
            fee_recipient="<sender>",
            price="500000",
            quantity="10",
            subaccount_id="<subaccount>",
          ),
        ),
      ],
      sequence=1,
      account_num=1234,
      chain_id="<chain-id>",
    )

    signed = self.wallet.sign(transaction)

    public_key = self.wallet.public_key
    signature = self.wallet.private_key.signing_key.to_der()

    public_key.verify(signed, signature)
