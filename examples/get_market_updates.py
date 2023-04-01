import time
import swagger_client
from swagger_client.rest import ApiException
from swagger_client import Configuration, MarketStatus
from pprint import pprint


import sys
import asyncio
import logging
import argparse
from os import environ
from argparse import Namespace
from typing import Optional, Tuple


def parse_cli_arguments()->Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("--id", help="frontrunner market id")
    parser.add_argument("--inj_id", help="injective market id")
    parser.add_argument("--prop_id", help="frontrunner prop id")
    parser.add_argument("--event_id", help="frontrunner sport event id")
    parser.add_argument("--league_id", help="frontrunner league id")
    args = parser.parse_args()
    return args

async def run_get_market(namespace: Namespace,  configuration:Configuration, status:Optional[MarketStatus]):
    api_instance = swagger_client.FrontrunnerApi(swagger_client.ApiClient(configuration))

    kwargs = {}
    for arg in vars(namespace):
        if getattr(namespace, arg):
            kwargs[arg] = getattr(namespace, arg)

    if status:
        kwargs['status'] = status

    try:
        api_response = api_instance.get_markets(**kwargs)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling FrontrunnerApi->get_markets: %s\n" % e)

async def main():

    frontrunner_api_key = environ.get('FRONTRUNNER_API_KEY')
    configuration = swagger_client.Configuration()
    configuration.api_key['Authorization'] = frontrunner_api_key
    namespace = parse_cli_arguments()
    status = swagger_client.MarketStatus()
    await run_get_market(namespace, configuration, status)



if __name__ == "__main__":
    pass