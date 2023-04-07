import logging

from typing import Optional

from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException
from frontrunner_sdk.logging.log_external_exceptions import log_external_exceptions # NOQA
from frontrunner_sdk.models.wallet import Wallet

logger = logging.getLogger(__name__)


class InjectiveLightClientDaemon:

  def __init__(self, base_url: Optional[str]):
    if base_url is None:
      raise FrontrunnerConfigurationException("No Injective light client daemon (lcd) base url configured")

    self.base_url = base_url

  @log_external_exceptions(__name__)
  async def initialize_wallet(self, wallet: Wallet) -> None:
    logger.debug("Calling Injective LCD to initialize wallet with wallet=%s", wallet.injective_address)

    try:
      await wallet.address.async_init_num_seq(self.base_url)

    except ValueError as cause:
      _, status = cause.args

      if status >= 500:
        raise FrontrunnerUnserviceableException(
          "Injective light client daemon (lcd) endpoint unavailable",
          base_url=self.base_url,
          address=wallet.injective_address,
        ) from cause

      else:
        raise FrontrunnerInjectiveException(
          "Could not initialize wallet",
          base_url=self.base_url,
          address=wallet.injective_address,
        ) from cause

    logger.debug(
      "Received response from Injective LCD yielding wallet=%s account_number=%d sequence=%d",
      wallet.injective_address,
      wallet.account_number,
      wallet.sequence,
    )
