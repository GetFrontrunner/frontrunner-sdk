from requests import get
from markets import Market, ActiveMarket, StagingMarket, factory
from typing import List, Union


def _get_all_markets() -> List[Union[ActiveMarket, StagingMarket, None]]:
    resp = get(
        "https://k8s.testnet.lcd.injective.network/injective/exchange/v1beta1/binary_options/markets"
    )
    data = resp.json()
    markets = data["markets"]
    return [factory(**market) for market in markets if factory(**market)]


def get_all_active_markets() -> List[ActiveMarket]:
    markets = _get_all_markets()
    return [market for market in markets if isinstance(market, ActiveMarket)]


def get_all_staging_markets() -> List[StagingMarket]:
    markets = _get_all_markets()
    return [market for market in markets if isinstance(market, StagingMarket)]
