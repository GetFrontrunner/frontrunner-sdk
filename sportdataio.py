import requests
import xmltodict
import pprint
import json
import aiohttp
import asyncio

# url = "https://sportsdata.io/developers/api-documentation/mlb#/endpoint/are-games-in-progress"
url = "https://api.sportsdata.io/v3/mlb/scores/json/AreAnyGamesInProgress"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingMetadata "
date = "2022"
url = f"https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/{date} "
season = "2023JAN"
url = f"https://api.sportsdata.io/v3/mlb/scores/json/Games/{season} "
url = "https://api.sportsdata.io/v3/mlb/scores/json/News"
url = f"https://api.sportsdata.io/v3/mlb/odds/json/BettingMetadata"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingEventsByDate/2020-8-20"
url = f"https://api.sportsdata.io/v3/mlb/odds/json/BettingEvents/2022STAR"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingFuturesBySeason/2022STAR"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingMarket/21"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingMarkets/12"
# this one doesnt work
# url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingMarketsByGameID/122"
url = "https://api.sportsdata.io/v3/mlb/odds/json/BettingMarketsByMarketType/21/2"
url = "https://api.sportsdata.io/v3/mlb/odds/json/LiveGameOddsByDate/2018-06-23"


def test(url):
    headers = {
        "Ocp-Apim-Subscription-Key": "f52ca5b9cb734f7b986b24e60bdd02dc",
    }

    a = requests.get(url, headers=headers)
    print(a.text)


async def test_2(url):
    headers = {
        "Ocp-Apim-Subscription-Key": "f52ca5b9cb734f7b986b24e60bdd02dc",
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            body = await r.json()
            print(len(body))
            print(body[0])
            # print(body[0])

            # print(body[0].get("BettingEventID"))
            # print(body[0].get("Name"))
            # print(body[0].get("Season"))
            # print(body[0].get("BettingEventTypeID"))
            # print(body[0].get("BettingEventType"))
            # print(body[0].get("StartDate"))
            # print(body[0].get("Created"))
            # print(body[0].get("Updated"))
            # print(body[0].get("GameID"))
            # print(body[0].get("GlobalGameID"))
            # print(body[0].get("GameStatus"))
            # print(body[0].get("Quarter"))
            # print(body[0].get("AwayTeam"))
            # print(body[0].get("HomeTeam"))
            # print(body[0].get("AwayTeamID"))
            # print(body[0].get("HomeTeamID"))
            # print(body[0].get("GlobalAwayTeamID"))
            # print(body[0].get("GlobalHomeTeamID"))
            # print(body[0].get("AwayTeamScore"))
            # print(body[0].get("HomeTeamScore"))
            # print(body[0].get("TotalScore"))
            # print(body[0].get("AwayRotationNumber"))
            # print(body[0].get("HomeRotationNumber"))
            # print(body[0].get("GameStartTime"))
            # print(body[0].get("BettingMarkets")[2].keys())
            # print(body[1].get("BettingMarkets").keys())
            # print(body[0].get("BettingMarkets")[0].keys())
            # print(body[0].get("BettingMarkets")[0]["AvailableSportsbooks"])
            # print(body[0].get("BettingMarkets")[0]["AnyBetsAvailable"])
            # print(body[0].get("Name"))
            # print(body[0].get("Season"))
            # print(body[0].get("BettingEventTypeID"))
            # print(body[0].get("BettingEventType"))
            # print(body[0].get("StartDate"))
            # print(body[0].get("Created"))
            # print(body[0].get("Updated"))
            # print(body[0].get("GameID"))
            # print(body[0].get("GlobalGameID"))
            # print(body[0].get("GameStatus"))
            # print(body[0].get("Quarter"))
            # print(body[0].get("AwayTeam"))
            # print(body[0].get("HomeTeam"))
            # print(body[0].get("AwayTeamID"))
            # print(body[0].get("HomeTeamID"))
            # print(body[0].get("GlobalAwayTeamID"))
            # print(body[0].get("GlobalHomeTeamID"))
            # print(body[0].get("AwayTeamScore"))
            # print(body[0].get("HomeTeamScore"))
            # print(body[0].get("TotalScore"))
            # print(body[0].get("AwayRotationNumber"))
            # print(body[0].get("HomeRotationNumber"))
            # print(body[0].get("GameStartTime"))
            # print(body[0].get("BettingMarkets"))
            # print(len(body[0].get("BettingMarkets")))
            # print(body[0].get("BettingMarkets")[0])
            # print(body[0].get("BettingMarkets")[1])
            # print(body[0].get("BettingMarkets")[-1])

        # print(body[0])
        # print(body.keys())
        # print(body["BettingBetTypes"][0])
        # print(body["BettingMarketTypes"][0])
        # print(body["BettingPeriodTypes"][0])
        # print(body["BettingEventTypes"][0])
        # print(body["BettingOutcomeTypes"][0])
        # print(body["ResultedMarketMetaData"][0])
        # print(body["BettingResultTypes"][0])


asyncio.run(test_2(url))
