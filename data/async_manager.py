import asyncio
import configparser
from utils.get_markets import get_all_active_markets, get_all_staging_markets

from data.betradar import BetRadarData
import logging

if __name__ == "__main__":
    logging.basicConfig(
        # filename="async_manager.log", encoding="utf-8", level=logging.DEBUG
        level=logging.INFO
    )

    loop = asyncio.get_event_loop()

    active_markets = get_all_active_markets()
    staging_markets = get_all_staging_markets()
    for staging_market in staging_markets:
        logging.info(staging_market)
    print()
    for active_market in active_markets:
        for market in active_markets[active_market]:
            logging.info(market.ticker)
        print()

    # matchbook = MatchbookData()
    # loop.run_until_complete(matchbook.get_sport())
    betradar = BetRadarData()
    loop.run_until_complete(betradar.get_probabilities_dummy())

    """
    betradar_prob_task = asyncio.create_task(betradar.get_probabilities_dummy())
    inj_data = InjectiveData(markets=active_market, granters=[])
    injective_trade_task = asyncio.create_task(inj_data.injective_trade_stream())
    loop.run_until_complete(asyncio.gather(betradar_prob_task, injective_trade_task))
    """

    loop.run_forever()
    loop.close()
