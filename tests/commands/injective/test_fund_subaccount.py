from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk import Wallet
from frontrunner_sdk.commands.injective.fund_subaccount import FundSubaccountOperation # NOQA
from frontrunner_sdk.commands.injective.fund_subaccount import FundSubaccountRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models import Subaccount
from frontrunner_sdk.models.order import Order


class TestFundSubaccountOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.subaccount = Subaccount.from_subaccount_id(self.subaccount_id)


  def test_validate(self):
    req = FundSubaccountRequest(amount=10, denom="FRCOIN", subaccount_index=0)
    cmd = FundSubaccountOperation(req)
    cmd.validate(self.deps)

  def test_validate_no_subaccount_exception(self):
    with self.assertRaises(FrontrunnerArgumentException):
      FundSubaccountOperation(FundSubaccountRequest(amount=10, denom="FRCOIN")).validate(self.deps)

  def test_validate_both_subaccounts_exception(self):
    with self.assertRaises(FrontrunnerArgumentException):
      FundSubaccountOperation(FundSubaccountRequest(amount=10, denom="FRCOIN", subaccount_index=0, subaccount=self.subaccount)).validate(self.deps)

  async def test_fund_subaccount(self):
    self.deps.injective_chain.fund_subaccount = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = FundSubaccountRequest(amount=10, denom="FRCOIN", subaccount=self.subaccount)
    cmd = FundSubaccountOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.fund_subaccount.assert_awaited_once_with(await self.deps.wallet(), self.subaccount_id, 10, "FRCOIN")

  async def test_fund_subaccount_by_index(self):
    subaccount_index = 2
    wallet = Wallet._new()
    subaccount = Subaccount.from_wallet_and_index(wallet, subaccount_index)

    self.deps.wallet = AsyncMock(return_value=wallet)
    self.deps.injective_chain.fund_subaccount = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = FundSubaccountRequest(amount=10, denom="FRCOIN", subaccount_index=subaccount_index)
    cmd = FundSubaccountOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.fund_subaccount.assert_awaited_once_with(await self.deps.wallet(), subaccount.subaccount_id, 10, "FRCOIN")
