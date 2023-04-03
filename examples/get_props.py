import asyncio
import argparse
from os import environ
from argparse import Namespace
from pprint import pprint
import swagger_client
from swagger_client.rest import ApiException
from swagger_client import Configuration 


def parse_cli_arguments() -> Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument("--id", help="frontrunner market id")
  parser.add_argument("--league_id", help="frontrunner league id")
  args = parser.parse_args()
  return args


async def run_get_props(namespace: Namespace, configuration: Configuration):
  api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))

  kwargs = {}
  for arg in vars(namespace):
    if getattr(namespace, arg):
      kwargs[arg] = getattr(namespace, arg)

  try:
    api_response = api_instance.get_props(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_props: %s\n" % e)


async def main():
  frontrunner_api_key = environ.get('FRONTRUNNER_API_KEY')
  configuration = swagger_client.Configuration()
  configuration.api_key['Authorization'] = frontrunner_api_key
  namespace = parse_cli_arguments()
  await run_get_props(namespace, configuration)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())