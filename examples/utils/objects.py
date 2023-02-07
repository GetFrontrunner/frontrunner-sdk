from enum import Enum
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
