from unittest import TestCase

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
