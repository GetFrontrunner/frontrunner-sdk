from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk import Wallet
from frontrunner_sdk.commands.injective.withdraw_from_subaccount import WithdrawFromSubaccountOperation # NOQA
from frontrunner_sdk.commands.injective.withdraw_from_subaccount import WithdrawFromSubaccountRequest # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC


class TestWithdrawFromSubaccountOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.wallet = Wallet._new()
    self.deps.wallet = AsyncMock(return_value=self.wallet)

  def test_validate(self):
    req = WithdrawFromSubaccountRequest(amount=10, denom="FRCOIN", subaccount_index=1)
    cmd = WithdrawFromSubaccountOperation(req)
    cmd.validate(self.deps)

  def test_validate_fails(self):
    with self.assertRaises(FrontrunnerArgumentException):
      WithdrawFromSubaccountOperation(WithdrawFromSubaccountRequest(amount=10, denom="FRCOIN",
                                                                    subaccount_index=0)).validate(self.deps)

    with self.assertRaises(FrontrunnerArgumentException):
      WithdrawFromSubaccountOperation(WithdrawFromSubaccountRequest(amount=10, denom="FRCOIN",
                                                                    subaccount_index=None)).validate(self.deps)

  async def test_withdraw_from_subaccount(self):
    subaccount_index = 1
    self.deps.injective_chain.withdraw_from_subaccount = AsyncMock(return_value=MagicMock(txhash="<txhash>"))

    req = WithdrawFromSubaccountRequest(
      amount=10,
      denom="FRCOIN",
      subaccount_index=subaccount_index,
    )
    cmd = WithdrawFromSubaccountOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.transaction, "<txhash>")

    self.deps.injective_chain.withdraw_from_subaccount.assert_awaited_once_with(
      await self.deps.wallet(), self.wallet.subaccount_address(subaccount_index), 10, "FRCOIN"
    )
