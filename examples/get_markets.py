import asyncio
import argparse
from os import environ
from argparse import Namespace
from typing import Optional
from pprint import pprint
from frontrunner_sdk.openapi.frontrunner_api import FrontrunnerApi, ApiClient
from frontrunner_sdk.openapi.frontrunner_api.rest import ApiException
from frontrunner_sdk.openapi.frontrunner_api import Configuration, MarketStatus


def parse_cli_arguments() -> Namespace:
  parser = argparse.ArgumentParser()

  parser.add_argument("--id", help="frontrunner market id")
  parser.add_argument("--inj_id", help="injective market id")
  parser.add_argument("--prop_id", help="frontrunner prop id")
  parser.add_argument("--event_id", help="frontrunner sport event id")
  parser.add_argument("--league_id", help="frontrunner league id")
  parser.add_argument("--status", help="frontrunner market status",choices=['active', 'closed'], default='active')
  args = parser.parse_args()
  return args

def valid_args(args):
  if (args['status']=='closed' and len(args)==1):
    raise Exception("Need to provide at least one of id, inj_id, prop_id, event_id, league_id when market status is closed")

async def run_get_markets(namespace: Namespace, configuration: Configuration):
  api_instance = FrontrunnerApi(ApiClient(configuration))

  kwargs = {}

  for arg in vars(namespace):
    if getattr(namespace, arg):
      if arg == 'status':
        if getattr(namespace, arg) == 'active':
          kwargs[arg] = MarketStatus.ACTIVE
        else:
          kwargs[arg] = MarketStatus.CLOSED
      else:
        kwargs[arg] = getattr(namespace, arg)

  valid_args(kwargs)

  try:
    api_response = api_instance.get_markets(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_markets: %s\n" % e)


async def main():
  frontrunner_api_key = environ.get('FRONTRUNNER_API_KEY')
  configuration = Configuration()
  configuration.api_key['Authorization'] = frontrunner_api_key
  namespace = parse_cli_arguments()
  if getattr(namespace, 'status')=="active":
    pass
  else:
    pass

    
  await run_get_markets(namespace, configuration)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
