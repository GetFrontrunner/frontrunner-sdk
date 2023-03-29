from dataclasses import dataclass
from typing import Iterable

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.wallet import Wallet


@dataclass
class CreateOrdersRequest:
  wallet: Wallet
  orders: Iterable[Order]


@dataclass
class CreateOrdersResponse:
  transaction: str


class CreateOrdersOperation(FrontrunnerOperation[CreateOrdersRequest, CreateOrdersResponse]):

  def __init__(self, request: CreateOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CreateOrdersResponse:
    response = await deps.injective_chain.create_orders(self.request.wallet, self.request.orders)
    return CreateOrdersResponse(transaction=response.txhash)
