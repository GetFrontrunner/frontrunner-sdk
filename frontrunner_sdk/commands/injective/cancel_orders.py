from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class CancelOrdersRequest:
  wallet: Wallet


@dataclass
class CancelOrdersResponse:
  transaction: str


class CancelAllOrdersOperation(FrontrunnerOperation[CancelOrdersRequest, CancelOrdersResponse]):

  def __init__(self, request: CancelOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CancelOrdersResponse:
    open_orders = await deps.injective_chain.get_all_open_orders(self.request.wallet)
    injective_market_ids = {order.market_id for order in open_orders}
    response = await deps.injective_chain.cancel_all_orders_for_markets(self.request.wallet, injective_market_ids)
    return CancelOrdersResponse(transaction=response.txhash)