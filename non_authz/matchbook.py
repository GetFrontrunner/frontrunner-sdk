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


url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=2000&sport-ids=15&states=open%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"
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
for event in events.events:
    print(event.name, event.id, event.volume, event.meta_tags)
    # print(event.id)
# print(len(res["events"]))
# for event in res["events"]:
#    if event["in-running-flag"]:
#        print(event["name"])
## print(res["events"])
##
