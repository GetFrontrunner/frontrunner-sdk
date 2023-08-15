from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import Tuple

from pyinjective.constant import Network
from pyinjective.orderhash import OrderHashManager
from pyinjective.proto.injective.exchange.v1beta1.exchange_pb2 import DerivativeOrder # NOQA

from frontrunner_sdk.models.wallet import Wallet


class InjectiveOrderHasher:

  def __init__(self, network: Network, wallet_fn: Callable[[], Awaitable[Wallet]]):
    self.network = network
    self.wallet_fn = wallet_fn
    self.hashers: Dict[Tuple[str, int], OrderHashManager] = {}

  def _hasher_for(self, wallet: Wallet, subaccount_index: int) -> OrderHashManager:
    if (wallet.injective_address, subaccount_index) not in self.hashers:
      self.hashers[wallet.injective_address, subaccount_index] = OrderHashManager(
        address=wallet.address,
        network=self.network,
        subaccount_indexes=[subaccount_index],
      )

    return self.hashers[wallet.injective_address, subaccount_index]

  async def hash(self, order: DerivativeOrder, subaccount_index: int) -> str:
    wallet = await self.wallet_fn()

    hasher = self._hasher_for(wallet, subaccount_index)

    response = hasher.compute_order_hashes([], [order], subaccount_index)

    return response.derivative[0]
