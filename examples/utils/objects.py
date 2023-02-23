from enum import Enum
from typing import Optional
from dataclasses import dataclass
from pyinjective.constant import Network


@dataclass
class BroadcastMode(Enum):
    ASYNC = 0
    SYNC = 1
    BLOCK = 2


@dataclass
class CustomNetwork:
    def __init__(
        self,
        lcd_endpoint: str,
        tm_endpoint: str,
        grpc_endpoint: str,
        exchange_endpoint: str,
        mainnet=False,
        mainnet_node="k8s",
    ):
        self.lcd_endpoint = lcd_endpoint
        self.source_network = Network.mainnet(mainnet_node) if mainnet else Network.testnet()
        self._network = Network(
            lcd_endpoint=lcd_endpoint,
            tm_websocket_endpoint=f"ws://{tm_endpoint}/websocket",
            grpc_endpoint=grpc_endpoint,
            grpc_exchange_endpoint=exchange_endpoint,
            grpc_explorer_endpoint=self.source_network.grpc_explorer_endpoint,
            # TODO: use Injective's API until we can run our own explorer container
            chain_id=self.source_network.chain_id,
            fee_denom=self.source_network.fee_denom,
            env=self.source_network.env,
        )

    @property
    def network(self) -> Network:
        return self._network


@dataclass
class OrderCreateRequest:
    subaccount_id: str
    market_id: str
    price: float
    quantity: int
    is_buy: bool
    is_po: bool
    is_reduce_only: bool


@dataclass
class OrderCancelRequest:
    subaccount_id: str
    market_id: str
    order_hash: str


@dataclass
class OrderCreateResponse:
    subaccount_id: str
    market_id: str
    price: float
    quantity: int
    is_buy: bool
    is_reduce_only: bool


@dataclass
class OrderCancelResponse:
    subaccount_id: str
    market_id: str
    order_hash: str


@dataclass
class OrderInfo:
    market_id: str
    side: str
    quantity: int
    price: float
    post_only: bool
    reduce_only: bool


@dataclass
class SubaccountOrdersRequest:
    subaccount_id: str
    market_id: str
    skip: Optional[int] = 0
    limit: Optional[int] = 100


@dataclass
class Order:
    order_hash: str
    side: str
    market_id: str
    subaccount_id: str
    margin: str
    price: str
    quantity: str
    unfilled_quantity: str
    trigger_price: str
    fee_recipient: str
    state: str
    created_at: int
    updated_at: int
    order_type: str
    is_conditional: bool
    execution_type: str


BinarySideMap = {"buy": True, "sell": False}

BiStateMarketMap = {"default": "0xb3a7e524c2ba5ec1eb44bf6780881d671992537eeab1428b8a44b205ceb3c304"}
MutiStateMarketMap = {
    "arsenal": "0x14be5f20eca7403929756b2333add97c1a4da3d49123664ef756c7a35b6e43e6",
    "chelsea": "0xc7c017e8b569eda649f4bcb51d71cee98de4f4e1fe33fcf341ba68afc4b3acb9",
    "draw": "0x4ab38f8ebea3a12acc08865990f3275fc5ab8f4662d3bd882c1840f434dae531",
}
