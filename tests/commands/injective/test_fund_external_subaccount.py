from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk import Wallet
from frontrunner_sdk.commands.injective.fund_external_subaccount import FundExternalSubaccountOperation # NOQA
from frontrunner_sdk.commands.injective.fund_external_subaccount import FundExternalSubaccountRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.models import Subaccount


class TestFundExternalSubaccountOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.destination_subaccount_id = "0xfddd3e6d98a236a1df56716ab8c407b1004113df000000000000000000000000"
    self.destination_subaccount = Subaccount.from_subaccount_id(self.destination_subaccount_id)
    self.wallet = Wallet._new()
    self.deps.wallet = AsyncMock(return_value=self.wallet)

  def test_validate(self):
    req = FundExternalSubaccountRequest(
      amount=10, denom="FRCOIN", source_subaccount_index=0, destination_subaccount=self.destination_subaccount
    )
    cmd = FundExternalSubaccountOperation(req)
    cmd.validate(self.deps)

  async def test_fund_external_subaccount_nonzero_source_index(self):
    source_subaccount_index = 1
    source_subaccount = Subaccount.from_wallet_and_index(self.wallet, source_subaccount_index)
    self.deps.injective_chain.fund_external_subaccount = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = FundExternalSubaccountRequest(
      amount=10,
      denom="FRCOIN",
      source_subaccount_index=source_subaccount_index,
      destination_subaccount=self.destination_subaccount
    )
    cmd = FundExternalSubaccountOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.fund_external_subaccount.assert_awaited_once_with(
      await self.deps.wallet(), source_subaccount.subaccount_id, self.destination_subaccount_id, 10, "FRCOIN"
    )

  async def test_fund_external_subaccount_from_bank_zero_index(self):
    self.deps.injective_chain.fund_subaccount_from_bank = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = FundExternalSubaccountRequest(
      amount=10, denom="FRCOIN", source_subaccount_index=0, destination_subaccount=self.destination_subaccount
    )
    cmd = FundExternalSubaccountOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.fund_subaccount_from_bank.assert_awaited_once_with(
      await self.deps.wallet(), self.destination_subaccount.subaccount_id, 10, "FRCOIN"
    )
