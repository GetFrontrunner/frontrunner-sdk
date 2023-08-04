from dataclasses import dataclass
from typing import Optional

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.helpers.validation import validate_mutually_exclusive
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models import Subaccount


@dataclass
class FundExternalSubaccountRequest:
  amount: int
  denom: str
  source_subaccount_index
  destination_subaccount: Subaccount


@dataclass
class FundExternalSubaccountResponse:
  transaction: str


class FundExternalSubaccountOperation(FrontrunnerOperation[FundExternalSubaccountRequest, FundExternalSubaccountResponse]):

  def __init__(self, request: FundExternalSubaccountRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> FundExternalSubaccountResponse:
    subaccount = self.request.destination_subaccount
    response = await deps.injective_chain.fund_subaccount(
      await deps.wallet(), subaccount.subaccount_id, self.request.amount, self.request.denom
    )

    return FundExternalSubaccountResponse(transaction=response.txhash)
