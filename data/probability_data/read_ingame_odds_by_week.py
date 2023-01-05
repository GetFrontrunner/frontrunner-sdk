import json
from odds import InGameOdds


f = open("./ingame_odds_by_week.json")
data = json.load(f)
ingame_odds = InGameOdds(data)
print("godd")
# print(data[0].keys())
# for d in data:
#    if d["AlternateMarketPregameOdds"]:
#        print(data[0]["AlternateMarketPregameOdds"])
#
