from requests import get
from typing import List, Union
from utils.markets import Market, ActiveMarket, StagingMarket, factory


def _get_all_markets(
    disable_error_msg: bool = False,
) -> List[Union[ActiveMarket, StagingMarket, None]]:
    resp = get(
        "https://k8s.testnet.lcd.injective.network/injective/exchange/v1beta1/binary_options/markets"
    )
    data = resp.json()
    markets = data["markets"]
    return [
        factory(disable_error_msg, **market)
        for market in markets
        if factory(disable_error_msg, **market)
    ]


def get_all_active_markets(disable_error_msg: bool = False) -> List[ActiveMarket]:
    markets = _get_all_markets(disable_error_msg)
    return [market for market in markets if isinstance(market, ActiveMarket)]


def get_all_staging_markets() -> List[StagingMarket]:
    markets = _get_all_markets()
    return [market for market in markets if isinstance(market, StagingMarket)]
