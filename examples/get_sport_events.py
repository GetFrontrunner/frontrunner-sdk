import asyncio
import argparse
from os import environ
from argparse import Namespace
from pprint import pprint
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi, ApiClient
from frontrunner_sdk.openapi.frontrunner_api.rest import ApiException
from frontrunner_sdk.openapi.frontrunner_api import Configuration, MarketStatus

def parse_cli_arguments() -> Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument("--id", help="frontrunner market id")
  parser.add_argument("--sport", help="frontrunner sport example")
  parser.add_argument("--league_id", help="frontrunner league id")
  parser.add_argument("--start_since", help="frontrunner start datetime E.g. 2013-10-20T19:20:30+01:00")
  args = parser.parse_args()
  return args


async def run_get_sport_events(namespace: Namespace, configuration: Configuration):
  api_instance = FrontrunnerApi(ApiClient(configuration))

  kwargs = {}
  for arg in vars(namespace):
    if getattr(namespace, arg):
      kwargs[arg] = getattr(namespace, arg)

  try:
    api_response = api_instance.get_sport_events(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_sport_events: %s\n" % e)


async def main():
  frontrunner_api_key = environ.get('FRONTRUNNER_API_KEY')
  configuration = Configuration()
  configuration.api_key['Authorization'] = frontrunner_api_key
  namespace = parse_cli_arguments()
  await run_get_sport_events(namespace, configuration)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
