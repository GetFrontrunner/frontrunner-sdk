from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging import log_operation


@dataclass
class CreateWalletRequest:
  pass


@dataclass
class CreateWalletResponse:
  pass


class CreateWalletOperation(FrontrunnerOperation[CreateWalletRequest, CreateWalletResponse]):

  def __init__(self, request: CreateWalletRequest):
    super().__init__(request)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CreateWalletResponse:
    # TODO
    return CreateWalletResponse()
