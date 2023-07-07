from configparser import ConfigParser
from typing import Dict
from typing import Optional

from pyinjective.constant import devnet_config
from pyinjective.constant import mainnet_config
from pyinjective.constant import testnet_config

from frontrunner_sdk.config.base import NetworkEnvironment
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.models.denom import Denom


class DenomFactory:

  def __init__(self, environment: Optional[NetworkEnvironment]):
    if not environment:
      raise FrontrunnerConfigurationException("No injective network configured")

    self.denoms = self._denoms_for_environment(environment)

  def __getitem__(self, name: str):
    if name not in self.denoms:
      raise FrontrunnerArgumentException("No such denom found", name=name, available=sorted(self.denoms.keys()))

    return self.denoms[name]

  def __contains__(self, name: str):
    return name in self.denoms

  @classmethod
  def _config_for(clz, environment: NetworkEnvironment) -> ConfigParser:
    if environment == "devnet":
      return devnet_config

    elif environment == "testnet":
      return testnet_config

    elif environment == "mainnet":
      return mainnet_config

    raise FrontrunnerConfigurationException(
      "Unsupported environment",
      environment=environment,
    )

  @classmethod
  def _denoms_for_environment(clz, environment: NetworkEnvironment) -> Dict[str, Denom]:
    denoms = [
      Denom(
        name=market,
        peggy=section.get("peggy_denom"),
        decimals=int(section.get("decimals")),
      ) for market, section in clz._config_for(environment).items() if "decimals" in section.keys()
    ]

    return {
      **{denom.name: denom
         for denom in denoms},
      **{denom.peggy: denom
         for denom in denoms},
    }
