import json

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from frontrunner_sdk.clients.injective_light_client_daemon import InjectiveLightClientDaemon # NOQA
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveLightClientDaemon(AioHTTPTestCase):

  def setUp(self):
    self.wallet = Wallet._new()
    self.wallet_info = web.Response()

  async def setUpAsync(self) -> None:
    await super().setUpAsync()

    self.injective_lcd_url = f"{self.server.scheme}://{self.server.host}:{self.server.port}"
    self.injective_lcd = InjectiveLightClientDaemon(self.injective_lcd_url)

  def get_wallet_info(self):

    async def handle(request: web.Request) -> web.Response:
      return self.wallet_info

    return handle

  async def get_application(self):
    # TODO this is an absolutely horrible way to configure tests; figure out something better
    app = web.Application()
    app.router.add_get("/cosmos/auth/v1beta1/accounts/{address}", self.get_wallet_info())

    return app

  def test_init_exception_when_missing_base_url(self):
    with self.assertRaises(FrontrunnerConfigurationException):
      InjectiveLightClientDaemon(None)

  async def test_initialize_wallet_success(self):
    self.wallet_info = web.Response(
      content_type="application/json",
      body=json.dumps({
        "account": {
          "base_account": {
            "account_number": "1234",
            "sequence": "2",
          },
        },
      }),
    )

    await self.injective_lcd.initialize_wallet(self.wallet)

    self.assertEqual(2, self.wallet.sequence)
    self.assertEqual(1234, self.wallet.account_number)

  async def test_initialize_wallet_failure_404(self):
    self.wallet_info = web.Response(status=404, text=json.dumps({"message": "Bad Request"}))

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_lcd.initialize_wallet(self.wallet)

  async def test_initialize_wallet_failure_503(self):
    self.wallet_info = web.Response(status=503, text=json.dumps({"message": "Service Unavailable"}))

    with self.assertRaises(FrontrunnerUnserviceableException):
      await self.injective_lcd.initialize_wallet(self.wallet)
