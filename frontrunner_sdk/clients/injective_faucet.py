import json
import logging

from typing import Optional

import aiohttp

from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.exceptions import FrontrunnerException
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException
from frontrunner_sdk.logging.log_external_exceptions import log_external_exceptions # NOQA
from frontrunner_sdk.models.wallet import Wallet # NOQA

logger = logging.getLogger(__name__)


class InjectiveFaucet:

  def __init__(self, base_url: Optional[str]):
    if base_url is None:
      raise FrontrunnerConfigurationException("No Injective faucet base url configured")

    self.base_url = base_url

  @log_external_exceptions(__name__)
  async def fund_wallet(self, wallet: Wallet) -> dict:
    async with aiohttp.ClientSession() as session:
      try:
        logger.debug("Calling Injective faucet to fund wallet with address=%s", wallet.injective_address)

        async with session.post(f"{self.base_url}?address={wallet.injective_address}") as response:
          # content type is sometimes text/plain and sometimes application/json, but is always json. Using .json() fails
          # whenever it's text/plain, so decoding manually as a workaround.
          body = json.loads(await response.text())

          if response.status >= 500:
            raise FrontrunnerUnserviceableException(
              body["message"],
              base_url=self.base_url,
              address=wallet.injective_address,
            )

          if not response.ok:
            raise FrontrunnerInjectiveException(
              body["message"],
              base_url=self.base_url,
              address=wallet.injective_address,
            )

          logger.debug("Received response from Injective faucet yielding message=%s", body["message"])

          return body

      except FrontrunnerException as exception:
        raise exception

      except Exception as cause:
        raise FrontrunnerUnserviceableException(
          "Could not fund wallet from faucet",
          base_url=self.base_url,
          address=wallet.injective_address,
        ) from cause
