import json
from odds import PreGameOdds

f = open("./pregame_odds_by_week.json")
data = json.load(f)
# print(len(data))

PreGameOdds(data)
print("good")
# print(data[0])
