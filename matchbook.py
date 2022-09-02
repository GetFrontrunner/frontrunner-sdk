# import requests
#
# url = "https://api.matchbook.com/edge/rest/navigation?offset=0&per-page=20"
#
# headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}
#
# response = requests.get(url, headers=headers)
#
## print(response.text)
## print(type(response.json()))
# for x in response.json():
#    for k, v in x.items():
#        print(k, " : ", v)


# import requests
#
# url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
#
# headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}
#
# response = requests.get(url, headers=headers)
#
# print(response.json())
url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&sport-ids=1231&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
from typing import Optional, Dict, Any

import requests
from data.matchbook.utilities import Events, Event

url = "https://api.matchbook.com/edge/rest/lookups/sports?offset=0&per-page=2000&order=name%20asc&status=active"
# url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=2000&states=open%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
##
headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}

response = requests.get(url, headers=headers)

res = response.json()
# for sport in res["sports"]:
#    print(sport["name"], sport["id"])


url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20000&states=open%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=true&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
response = requests.get(url, headers=headers)

res = response.json()
# print(res["events"][0])
in_running_flag_events = [event for event in res["events"] if event["in-running-flag"]]
# print(in_running_flag_events[-1])
# for event in in_running_flag_events:
#    print(event)
#    break
events = Events(res["events"])
# print(len(events.events))


def check_false(event_id: int):
    url = f"https://api.matchbook.com/edge/rest/events/{event_id}?exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"

    headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}

    response_false = requests.get(url, headers=headers).json()
    return response_false


def check_true(event_id: int):
    url = f"https://api.matchbook.com/edge/rest/events/{event_id}?exchange-type=back-lay&odds-type=DECIMAL&include-prices=true&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"

    headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}

    response_true = requests.get(url, headers=headers).json()
    return response_true


# print(response_false == response_true)

# print(False)
def compare(response_false: Dict[str, Any], response_true: Dict[str, Any]) -> bool:
    for ((kf, vf), (kt, vt)) in zip(response_false.items(), response_true.items()):
        if vf != vt:
            # print(kf, kt, vf, vf)
            print(response_false["id"], " ", kf, " ", kt, len(vf), " ", len(vt))
            # print(vf)
            # print(vt)
            if len(vf) == 1:
                return False
    return True
    # print(kf, kt, " ", vf == vt)


seens = []
for event in events.events:
    # print(event.name, event.id, event.volume, event.meta_tags)

    try:
        if event.id and event.id not in seens:
            response_false = check_false(event.id)
            response_true = check_true(event.id)
            resp = compare(response_false, response_true)
            seens.append(event.id)
            if not resp:
                break

        # print(
        #    event.id,
        #    event.sport_id,
        #    event.markets[0].runners[0].prices[0].currency,
        #    event.markets[0].runners[0].prices[0].odds,
        # )
        # break
    except:
        pass


event_id = 2160216931290016
response_false = check_false(event_id)
response_true = check_true(event_id)
# for market in response_false["markets"]:
#    for k, v in market.items():
#        print(f"{k}\t {v}")
# for market in response_true["markets"]:
#    for k, v in market.items():
#        print(f"{k}\t {v}")
for ((kf, vf), (kt, vt)) in zip(
    response_false["markets"][0].items(), response_true["markets"][0].items()
):
    if vf != vt:
        print(vf, vt)
        # print(len(vf), "==", len(vt))
        # if len(vf) == len(vt):
        #    for i in range(len(vf)):
        #        for ((kvf, vvf), (kft, vvt)) in zip(vf[i].items(), vt[i].items()):
        #            if vvf != vvt:
        #                print(kvf)
        #                print(vvf)
        #                print(vvt)

# print(kf, kt, kf == kt)
# resp = compare(response_false, response_true)

# print(event.sport_id, event.id, event.markets[0].runners[0].prices)
# print(event.id)
# print(len(res["events"]))
# for event in res["events"]:
#    if event["in-running-flag"]:
#        print(event["name"])
## print(res["events"])
##

# print(response_false["markets"][0])
# print(response_true["markets"][0])
