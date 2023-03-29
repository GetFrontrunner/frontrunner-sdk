import json
from unittest.mock import patch

from aiohttp import ClientError
from aiohttp import ClientSession
from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException
from frontrunner_sdk.exceptions import FrontrunnerInjectiveException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException
from frontrunner_sdk.models.wallet import Wallet


class TestInjectiveFaucet(AioHTTPTestCase):

  def setUp(self):
    self.wallet = Wallet._new()
    self.fund_wallet_response = web.Response()

  async def setUpAsync(self) -> None:
    await super().setUpAsync()

    self.injective_faucet = InjectiveFaucet(f"{self.server.scheme}://{self.server.host}:{self.server.port}")

  def post_fund_wallet(self):

    async def handle(request: web.Request) -> web.Response:
      return self.fund_wallet_response

    return handle

  async def get_application(self):
    # TODO this is an absolutely horrible way to configure tests; figure out something better
    app = web.Application()
    app.router.add_post("/", self.post_fund_wallet())

    return app

  def test_init_exception_when_missing_base_url(self):
    with self.assertRaises(FrontrunnerConfigurationException):
      InjectiveFaucet(None)

  async def test_fund_wallet_success(self):
    self.fund_wallet_response = web.Response(text=json.dumps({"message": "Works"}))

    res = await self.injective_faucet.fund_wallet(self.wallet)
    self.assertEquals(res, {"message": "Works"})

  async def test_fund_wallet_failure(self):
    self.fund_wallet_response = web.Response(status=400, text=json.dumps({"message": "Bad Request"}))

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_faucet.fund_wallet(self.wallet)

  async def test_fund_wallet_unserviceable_server_error(self):
    self.fund_wallet_response = web.Response(status=500, text=json.dumps({"message": "Internal Server Error"}))

    with self.assertRaises(FrontrunnerUnserviceableException):
      await self.injective_faucet.fund_wallet(self.wallet)

  async def test_fund_wallet_unserviceable_infrastructure(self):
    with patch.object(ClientSession, "post") as _post:
      _post.side_effect = ClientError("Bad URL")

      with self.assertRaises(FrontrunnerUnserviceableException):
        await self.injective_faucet.fund_wallet(self.wallet)
