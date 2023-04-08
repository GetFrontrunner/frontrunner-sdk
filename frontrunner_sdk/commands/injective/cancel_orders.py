from dataclasses import dataclass

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class CancelAllOrdersRequest:
  pass


@dataclass
class CancelAllOrdersResponse:
  transaction: str


class CancelAllOrdersOperation(FrontrunnerOperation[CancelAllOrdersRequest, CancelAllOrdersResponse]):

  def __init__(self, request: CancelAllOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CancelAllOrdersResponse:
    wallet = await deps.wallet()

    open_orders = await deps.injective_chain.get_all_open_orders(wallet)

    injective_market_ids = {order.market_id for order in open_orders}

    response = await deps.injective_chain.cancel_all_orders_for_markets(wallet, injective_market_ids)

    return CancelAllOrdersResponse(transaction=response.txhash)
