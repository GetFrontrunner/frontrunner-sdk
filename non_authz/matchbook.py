from data.matchbook.data import MatchbookData
from utils.get_markets import get_all_active_markets
import asyncio

# all_active_markets = get_all_active_markets()
# for market in all_active_markets:
#    print(market.activate_market)
data = MatchbookData()
print("good")

print("closed: ", data.session.closed)


async def close(session):
    print("closed: ", session.closed)
    await session.close()
    print("closed: ", session.closed)


asyncio.run(data.close())
print("end")
