from abc import ABC
from abc import abstractmethod

from google.protobuf.message import Message


class GasEstimator(ABC):

  @abstractmethod
  async def gas_for(self, message: Message) -> int:
    pass
