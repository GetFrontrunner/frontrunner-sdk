from typing import Callable
from typing import List
from typing import Optional
from typing import TypeVar

from frontrunner_sdk.config.base import FrontrunnerConfig

T = TypeVar("T")


class ChainedFrontrunnerConfig(FrontrunnerConfig):

  def __init__(self, configs: List[FrontrunnerConfig]):
    self.configs = configs

  def _find_next(self, get_value: Callable[[FrontrunnerConfig], Optional[T]]) -> Optional[T]:
    for config in self.configs:
      value = get_value(config)

      if value is not None:
        return value

    return None

  @property
  def injective_exchange_endpoint(self) -> Optional[str]:
    return self._find_next(lambda config: config.injective_exchange_endpoint)

  @property
  def injective_grpc_endpoint(self) -> Optional[str]:
    return self._find_next(lambda config: config.injective_grpc_endpoint)

  @property
  def injective_lcd_endpoint(self) -> Optional[str]:
    return self._find_next(lambda config: config.injective_lcd_endpoint)

  @property
  def injective_rpc_endpoint(self) -> Optional[str]:
    return self._find_next(lambda config: config.injective_rpc_endpoint)

  @property
  def injective_faucet_base_url(self) -> Optional[str]:
    return self._find_next(lambda config: config.injective_faucet_base_url)
