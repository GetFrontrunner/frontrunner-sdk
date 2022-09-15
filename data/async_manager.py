import asyncio
import configparser
from utils.get_markets import get_all_active_markets, get_all_staging_markets

# from data.injective import InjectiveData
from data.matchbook import MatchbookData
import logging

# https://googleapis.dev/python/pubsub/latest/subscriber/index.html

if __name__ == "__main__":
    logging.basicConfig(
        # filename="async_manager.log", encoding="utf-8", level=logging.DEBUG
        level=logging.INFO
    )
    configs = configparser.ConfigParser()
    configs.read("../configs/config_guild_1.ini")

    loop = asyncio.get_event_loop()

    active_markets = get_all_active_markets()
    staging_markets = get_all_staging_markets()
    for staging_market in staging_markets:
        logging.info(staging_market.ticker)
    for active_market in active_markets:
        logging.info(active_market.ticker)

    # inj_data = InjectiveData(
    #    markets=active_market, granters=[], redis_addr="127.0.0.1:6379"
    # )

    # loop.create_task(inj_data.injective_trade_stream())
    matchbook = MatchbookData()
    # loop.run_until_complete(matchbook.get_sport())
    loop.run_until_complete(matchbook.get_events(4))

    loop.run_forever()
    loop.close()
