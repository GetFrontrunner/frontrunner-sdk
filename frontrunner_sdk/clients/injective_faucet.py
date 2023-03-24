import json
import logging
from typing import Optional

import aiohttp

from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException

logger = logging.getLogger(__name__)


class InjectiveFaucet:

  def __init__(self, base_url: Optional[str]):
    if base_url is None:
      raise FrontrunnerConfigurationException("No Injective faucet base url configured")

    self.base_url = base_url

  async def fund_wallet(self, address: str) -> dict:
    async with aiohttp.ClientSession() as session:
      async with session.post(f"{self.base_url}?address={address}") as response:
        # content type is always text/plain, so .json() won't work
        body = json.loads(await response.text())

        # TODO handle 500

        if not response.ok:
          raise FrontrunnerInjectiveException(body["message"], address=address)

        return body
