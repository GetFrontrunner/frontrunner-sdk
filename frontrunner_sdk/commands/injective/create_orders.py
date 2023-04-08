from dataclasses import dataclass
from typing import List

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation
from frontrunner_sdk.models.order import Order


@dataclass
class CreateOrdersRequest:
  orders: List[Order]


@dataclass
class CreateOrdersResponse:
  transaction: str


class CreateOrdersOperation(FrontrunnerOperation[CreateOrdersRequest, CreateOrdersResponse]):

  def __init__(self, request: CreateOrdersRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    if not len(self.request.orders):
      raise FrontrunnerArgumentException("Orders cannot be empty")

    for order in self.request.orders:
      if order.quantity <= 0:
        raise FrontrunnerArgumentException("Order quantity must be > 0", order=order)

      if order.price <= 0 or 1 <= order.price:
        raise FrontrunnerArgumentException("Order price must be within between 0 and 1 exclusive", order=order)

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> CreateOrdersResponse:
    response = await deps.injective_chain.create_orders(await deps.wallet(), self.request.orders)

    return CreateOrdersResponse(transaction=response.txhash)
