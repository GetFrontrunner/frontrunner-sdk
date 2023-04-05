import asyncio
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple
from pprint import pprint

from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi, ApiClient
from frontrunner_sdk.openapi.frontrunner_api.rest import ApiException
from frontrunner_sdk.openapi.frontrunner_api import Configuration, MarketStatus
from frontrunner_sdk.ioc import FrontrunnerIoC

def parse_cli_arguments() -> Namespace:

  parser = argparse.ArgumentParser()
  parser.add_argument("--id", help="frontrunner market id")
  parser.add_argument("--sport", help="frontrunner sport")
  args = parser.parse_args()
  return args


async def run_get_leagues(namespace: Namespace, configuration: Configuration):
  app = FrontrunnerIoC()
  api_instance = app.openapi_frontrunner_api
  api_instance = FrontrunnerApi(ApiClient(configuration))

  kwargs = {}
  for arg in vars(namespace):
    if getattr(namespace, arg):
      kwargs[arg] = getattr(namespace, arg)

  try:
    api_response = api_instance.get_leagues(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_leagues: %s\n" % e)


async def main():

  frontrunner_api_key = environ.get('FRONTRUNNER_API_KEY')
  configuration = Configuration()
  configuration.api_key['Authorization'] = frontrunner_api_key
  namespace = parse_cli_arguments()
  await run_get_leagues(namespace, configuration)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
