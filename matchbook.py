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

url = "https://api.matchbook.com/edge/rest/events?offset=0&per-page=20&states=open%2Csuspended%2Cclosed%2Cgraded&exchange-type=back-lay&odds-type=DECIMAL&include-prices=false&price-depth=3&price-mode=expanded&include-event-participants=false&exclude-mirrored-prices=false"

headers = {"Accept": "application/json", "User-Agent": "api-doc-test-client"}

response = requests.get(url, headers=headers)

res = response.json()
# print(res["events"][0])
# print()
for k, v in res["events"][1]["markets"][0].items():
    if k == "runners":
        for key, val in v[0].items():
            print("@@ ", key, "   :  ", val)
