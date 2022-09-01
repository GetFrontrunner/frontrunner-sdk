import asyncio
import configparser
from utils.get_markets import get_all_active_markets, get_all_staging_markets
from data.injective import InjectiveData

# https://googleapis.dev/python/pubsub/latest/subscriber/index.html

if __name__ == "__main__":
    configs = configparser.ConfigParser()
    configs.read("../configs/config_guild_1.ini")

    loop = asyncio.get_event_loop()

    active_market = get_all_active_markets()
    staging_market = get_all_staging_markets()

    inj_data = InjectiveData(
        markets=active_market, granters=[], redis_addr="127.0.0.1:6379"
    )

    loop.create_task(inj_data.injective_trade_stream())

    loop.run_forever()
    loop.close()
