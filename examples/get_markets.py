import asyncio
import click
from pprint import pprint

from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.rest import ApiException


@click.group()
def cli():
    pass


@click.command()
@click.option("--id", help="frontrunner market id", type=str)
@click.option("--inj_id", help="injective market id", type=str)
@click.option("--prop_id", help="frontrunner prop id", type=str)
@click.option("--event_id", help="frontrunner sport event id", type=str)
@click.option("--league_id", help="frontrunner league id", type=str)
def active(**kwargs):
  parameters = {}
  for key, value in kwargs.items():
    if value is not None:
      parameters[key] = value
  return parameters


@click.command()
@click.option("--id", help="frontrunner market id", type=str)
@click.option("--inj_id", help="injective market id", type=str)
@click.option("--prop_id", help="frontrunner prop id", type=str)
@click.option("--event_id", help="frontrunner sport event id", type=str)
@click.option("--league_id", help="frontrunner league id", type=str)
def closed(**kwargs):
    if any(value is not None for value in kwargs.values()):
        parameters = {}
        for key, value in kwargs.items():
            if value is not None:
                parameters[key]=value
        return parameters
    else:
        raise click.exceptions.MissingParameter("closed market requires at least 1 option")


cli.add_command(active)
cli.add_command(closed)


async def run_get_markets(**kwargs):
  app = FrontrunnerIoC()
  api_instance = app.openapi_frontrunner_api

  try:
    api_response = await api_instance.get_markets(**kwargs)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling FrontrunnerApi->get_markets: %s\n" % e)


async def main():
  cli_params = cli(standalone_mode=False)
  await run_get_markets(**cli_params)


if __name__ == "__main__":
  asyncio.get_event_loop().run_until_complete(main())
