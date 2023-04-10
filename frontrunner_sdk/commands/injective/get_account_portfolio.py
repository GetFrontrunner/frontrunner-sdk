from dataclasses import dataclass

from pyinjective.proto.exchange.injective_portfolio_rpc_pb2 import Portfolio

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetAccountPortfolioRequest:
  pass


@dataclass
class GetAccountPortfolioResponse:
  portfolio: Portfolio


class GetAccountPortfolioOperation(FrontrunnerOperation[GetAccountPortfolioRequest, GetAccountPortfolioResponse]):

  def __init__(self, request: GetAccountPortfolioRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetAccountPortfolioResponse:
    wallet = await deps.wallet()

    # for now, this is a straight proxy call, and we return the raw result;
    # return may be augmented in the future.
    get_account_portfolio = await deps.injective_client.get_account_portfolio(wallet.injective_address)

    return GetAccountPortfolioResponse(portfolio=get_account_portfolio.portfolio)
