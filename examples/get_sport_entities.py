import asyncio
import click
from pprint import pprint
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.rest import ApiException


@click.command()
@click.option("--id", help="frontrunner market id", type=str)
@click.option("--sport", help="frontrunner sport", type=str)
@click.option("--league_id", help="frontrunner league id", type=str)
def cli(**kwargs):
  parameters = {}
  for key, value in kwargs.items():
    if value is not None:
      parameters[key] = value
  return parameters


async def run_get_sport_entities(**kwargs):
  app = FrontrunnerIoC()
  api_instance = app.openapi_frontrunner_api

  try:
    api_response = await api_instance.get_sport_events(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_sport_entities: %s\n" % e)


async def main():
  cli_params = cli(standalone_mode=False)
  await run_get_sport_entities(**cli_params)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
