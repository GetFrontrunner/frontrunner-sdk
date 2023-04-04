import logging

from typing import Tuple
from unittest import IsolatedAsyncioTestCase

from frontrunner_sdk.clients.openapi_client import api_methods
from frontrunner_sdk.clients.openapi_client import openapi_client
from frontrunner_sdk.clients.openapi_client import with_debug_logging
from frontrunner_sdk.clients.openapi_client import with_exception
from frontrunner_sdk.exceptions import FrontrunnerArgumentException
from frontrunner_sdk.exceptions import FrontrunnerUnserviceableException


class ExampleApi:

  def __init__(self, name: str):
    self.name = name

  def __str__(self) -> str:
    return self.__class__.__name__

  async def respond_good(self, a: str, b: int, c: bool = False) -> dict:
    (response, _, _) = await self.respond_good_with_http_info(a, b, c=c)
    return response

  async def respond_good_with_http_info(self, a: str, b: int, c: bool = False) -> Tuple[dict, int, dict]:
    return ({"a": a, "b": b, "c": c}, 200, {})

  async def respond_server_error(self, a: str, b: int, c: bool = False) -> dict:
    (response, _, _) = await self.respond_server_error_with_http_info(a, b, c=c)
    return response

  async def respond_server_error_with_http_info(self, a: str, b: int, c: bool = False) -> Tuple[dict, int, dict]:
    return ({"a": a, "b": b, "c": c}, 500, {})

  async def respond_client_error(self, a: str, b: int, c: bool = False) -> dict:
    (response, _, _) = await self.respond_client_error_with_http_info(a, b, c=c)
    return response

  async def respond_client_error_with_http_info(self, a: str, b: int, c: bool = False) -> Tuple[dict, int, dict]:
    return ({"a": a, "b": b, "c": c}, 400, {})

  async def respond_exception(self) -> dict:
    (response, _, _) = await self.respond_exception_with_http_info()
    return response

  async def respond_exception_with_http_info(self) -> Tuple[dict, int, dict]:
    raise Exception("BOOM")


class TestOpenAPIClient(IsolatedAsyncioTestCase):

  def setUp(self):
    self.api = ExampleApi("example")

  def test_api_methods(self):
    response = dict(api_methods(ExampleApi))

    method_names = response.keys()

    self.assertEqual(
      method_names,
      set(["respond_good", "respond_server_error", "respond_client_error", "respond_exception"]),
    )

    self.assertEqual(response["respond_good"], ExampleApi.respond_good_with_http_info)
    self.assertEqual(response["respond_server_error"], ExampleApi.respond_server_error_with_http_info)
    self.assertEqual(response["respond_client_error"], ExampleApi.respond_client_error_with_http_info)
    self.assertEqual(response["respond_exception"], ExampleApi.respond_exception_with_http_info)

  async def test_with_exception_good(self):
    method = with_exception(self.api.respond_good_with_http_info)
    result, _ = await method("hello", 123, True)

    self.assertEqual(result, {
      "a": "hello",
      "b": 123,
      "c": True,
    })

    self.assertEqual(method.__wrapped__, self.api.respond_good_with_http_info)

  async def test_with_exception_server_error(self):
    method = with_exception(self.api.respond_server_error_with_http_info)

    with self.assertRaises(FrontrunnerUnserviceableException):
      await method("hello", 123, c=True)

  async def test_with_exception_client_error(self):
    method = with_exception(self.api.respond_client_error_with_http_info)

    with self.assertRaises(FrontrunnerArgumentException):
      await method("hello", 123, c=True)

  async def test_with_exception_exception(self):
    method = with_exception(self.api.respond_exception_with_http_info)

    with self.assertRaises(FrontrunnerUnserviceableException):
      await method("hello", 123, c=True)

  async def test_with_debug_logging(self):
    method = with_debug_logging(self.api, self.api.respond_good_with_http_info)

    self.assertEqual(method.__wrapped__, self.api.respond_good_with_http_info)

    with self.assertLogs(level=logging.DEBUG) as logs:
      await method("hello", 123, c=True)

      messages = [record.getMessage() for record in logs.records]

      self.assertRegexpMatches(messages[0], r"^Calling OpenAPI\[ExampleApi\] to respond_good")
      self.assertRegexpMatches(messages[1], r"^Received response from OpenAPI\[ExampleApi\] respond_good")

  async def test_openapi_client(self):
    wrapped = openapi_client(ExampleApi, "a-name")

    self.assertIsInstance(wrapped, ExampleApi)
    self.assertEqual(wrapped.name, "a-name")

    method = wrapped.respond_good

    while hasattr(method, "__wrapped__"):
      method = method.__wrapped__

    self.assertEqual(method, ExampleApi.respond_good_with_http_info)
