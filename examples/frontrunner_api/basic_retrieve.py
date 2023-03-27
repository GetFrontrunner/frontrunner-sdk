import os
from typing import List

import swagger_client
from swagger_client import League
from swagger_client.rest import ApiException


def main_swagger(base_url, token):
    configuration = swagger_client.Configuration()
    configuration.host = base_url
    api_client = swagger_client.ApiClient(configuration, header_name="Authorization", header_value=token)
    api_instance = swagger_client.FrontrunnerApi(api_client)

    try:
        leagues: List[League] = api_instance.get_leagues()
        print(leagues)
        league_id = leagues[0].id
        print(league_id)
        print(api_instance.get_markets(league_id=league_id))
        print(api_instance.get_sport_events(league_id=league_id))
        print(api_instance.get_sport_entities(league_id=league_id))
    except ApiException as e:
        print("Exception when calling FrontrunnerApi: %s\n" % e)


def main():
    base_url = f"https://partner-api.getfrontrunner.com/api/v1"
    token = os.environ["FRONTRUNNER_API_KEY"]
    main_swagger(base_url, token)


if __name__ == "__main__":
    main()
