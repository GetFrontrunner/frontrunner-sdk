from data.cefi_data import CefiData
from data.injective_data import InjectiveData
import asyncio
import configparser
from utils.markets import factory
from utils.get_markets import get_all_active_markets, get_all_staging_markets

# https://googleapis.dev/python/pubsub/latest/subscriber/index.html

if __name__ == "__main__":
    configs = configparser.ConfigParser()
    configs.read("../configs/config_guild_1.ini")

    loop = asyncio.get_event_loop()

    active_market = get_all_active_markets()
    staging_market = get_all_staging_markets()
    # granted_markets = [
    #    build_granted_market(
    #        configs[section].get("base").upper(),
    #        configs[section].get("quote").upper(),
    #        section.split("_")[0].upper(),
    #    )
    #    for section in configs.sections()
    #    if "market" in section.lower()
    # ]
    inj_data = InjectiveData(markets=active_market, redis_addr="127.0.0.1:6379")

    loop.create_task(inj_data.injective_trade_stream_perp())

    loop.run_forever()
    loop.close()
