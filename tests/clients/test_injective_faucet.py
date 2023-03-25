import json

from aiohttp import web
from aiohttp.test_utils import AioHTTPTestCase

from frontrunner_sdk.clients.injective_faucet import InjectiveFaucet
from frontrunner_sdk.exceptions import FrontrunnerConfigurationException, FrontrunnerInjectiveException


class TestInjectiveFaucet(AioHTTPTestCase):

  def setUp(self):
    self.fund_wallet_response = web.Response()

  async def setUpAsync(self) -> None:
    await super().setUpAsync()

    self.injective_faucet = InjectiveFaucet(f"{self.server.scheme}://{self.server.host}:{self.server.port}")

  def post_fund_wallet(self):
    async def handle(request: web.Request) -> web.Response:
      return self.fund_wallet_response

    return handle

  async def get_application(self):
    app = web.Application()
    app.router.add_post("/", self.post_fund_wallet())

    return app

  def test_init_exception_when_missing_base_url(self):
    with self.assertRaises(FrontrunnerConfigurationException):
      InjectiveFaucet(None)

  async def test_fund_wallet_success(self):
    self.fund_wallet_response = web.Response(text=json.dumps({"message": "Works"}))

    res = await self.injective_faucet.fund_wallet(address="<fake>")
    self.assertEquals(res, {"message": "Works"})

  async def test_fund_wallet_error(self):
    self.fund_wallet_response = web.Response(status=500, text=json.dumps({"message": "Works"}))

    with self.assertRaises(FrontrunnerInjectiveException):
      await self.injective_faucet.fund_wallet(address="<fake>")
