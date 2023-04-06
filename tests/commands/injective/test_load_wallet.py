from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.injective.load_wallet import LoadWalletFromMnemonicOperation, LoadWalletFromPrivateKeyRequest, \
  LoadWalletFromPrivateKeyOperation  # NOQA
from frontrunner_sdk.commands.injective.load_wallet import LoadWalletFromMnemonicRequest # NOQA
from frontrunner_sdk.commands.injective.load_wallet import LoadWalletFromMnemonicResponse # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models.wallet import Wallet


class TestLoadWalletFromMnemonicOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.mnemonic = self.wallet.mnemonic
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate(self):
    req = LoadWalletFromMnemonicRequest(mnemonic=self.mnemonic)
    cmd = LoadWalletFromMnemonicOperation(req)
    cmd.validate(self.deps)

  async def test_load_wallet_from_mnemonic(self):
    self.deps.injective_light_client_daemon.initialize_wallet = AsyncMock()

    req = LoadWalletFromMnemonicRequest(mnemonic=self.mnemonic)
    cmd = LoadWalletFromMnemonicOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.wallet.mnemonic, self.wallet.mnemonic)
    self.assertEqual(res.wallet.private_key.to_hex(), self.wallet.private_key.to_hex())

    self.deps.injective_light_client_daemon.initialize_wallet.assert_awaited_once()


class TestLoadWalletFromPrivateKeyOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.wallet = Wallet._new()
    self.private_key = self.wallet.private_key
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def test_validate(self):
    req = LoadWalletFromPrivateKeyRequest(private_key=self.private_key)
    cmd = LoadWalletFromPrivateKeyOperation(req)
    cmd.validate(self.deps)

  async def test_load_wallet_from_private_key(self):
    self.deps.injective_light_client_daemon.initialize_wallet = AsyncMock()

    req = LoadWalletFromPrivateKeyRequest(private_key=self.private_key.to_hex())
    cmd = LoadWalletFromPrivateKeyOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.wallet.private_key.to_hex(), self.wallet.private_key.to_hex())

    self.deps.injective_light_client_daemon.initialize_wallet.assert_awaited_once()
