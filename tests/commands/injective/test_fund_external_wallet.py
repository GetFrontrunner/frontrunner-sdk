from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk import Wallet
from frontrunner_sdk.commands.injective.fund_external_wallet import FundExternalWalletOperation # NOQA
from frontrunner_sdk.commands.injective.fund_external_wallet import FundExternalWalletRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestFundExternalWalletOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.wallet = Wallet._new()
    self.deps.wallet = AsyncMock(return_value=self.wallet)
    self.destination_injective_address = "inj1fjlfjy5adns4msjqch3vqjhesmwjnu9ep045wz"

  def test_validate(self):
    req = FundExternalWalletRequest(
      amount=10, denom="FRCOIN", destination_injective_address=self.destination_injective_address
    )
    cmd = FundExternalWalletOperation(req)
    cmd.validate(self.deps)

  async def test_fund_external_wallet(self):
    self.deps.injective_chain.fund_external_wallet_from_bank = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = FundExternalWalletRequest(
      amount=10, denom="FRCOIN", destination_injective_address=self.destination_injective_address
    )
    cmd = FundExternalWalletOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.fund_external_wallet_from_bank.assert_awaited_once_with(
      await self.deps.wallet(), self.destination_injective_address, 10, "FRCOIN"
    )
