from dataclasses import dataclass
from typing import Iterable
from typing import Mapping

from pyinjective.proto.exchange.injective_derivative_exchange_rpc_pb2 import DerivativeLimitOrderbookV2 # NOQA

from frontrunner_sdk.commands.base import FrontrunnerOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.logging.log_operation import log_operation


@dataclass
class GetOrderBooksRequest:
  market_ids: Iterable[str]


@dataclass
class GetOrderBooksResponse:
  order_books: Mapping[str, DerivativeLimitOrderbookV2]


class GetOrderBooksOperation(FrontrunnerOperation[GetOrderBooksRequest, GetOrderBooksResponse]):

  def __init__(self, request: GetOrderBooksRequest):
    super().__init__(request)

  def validate(self, deps: FrontrunnerIoC) -> None:
    pass

  @log_operation(__name__)
  async def execute(self, deps: FrontrunnerIoC) -> GetOrderBooksResponse:
    get_derivative_orderbooks = await deps.injective_client.get_derivative_orderbooksV2(self.request.market_ids)

    order_books = {order_book.market_id: order_book.orderbook for order_book in get_derivative_orderbooks.orderbooks}

    return GetOrderBooksResponse(order_books=order_books)
