from requests import get
from typing import List, Union, Dict
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


def get_all_active_markets(
    disable_error_msg: bool = False,
) -> Dict[str, List[ActiveMarket]]:
    markets = _get_all_markets(disable_error_msg)
    tmp_markets_dict = {}
    for market in markets:
        if market and isinstance(market, ActiveMarket) and market.ticker:
            key = "-".join(market.ticker.split("-")[:2])
            if tmp_markets_dict.get(key):
                pass
            else:
                tmp_markets_dict[key] = []
            tmp_markets_dict[key].append(market)

    # print(markets_dict)
    markets_dict = {key: tmp_markets_dict[key] for key in sorted(tmp_markets_dict)}

    return markets_dict  # [market for market in markets if isinstance(market, ActiveMarket)]


def get_all_staging_markets() -> Dict[str, List[StagingMarket]]:
    markets = _get_all_markets()
    # return [market for market in markets if isinstance(market, StagingMarket)]

    markets_dict = {}
    for market in markets:
        if market and isinstance(market, StagingMarket) and market.ticker:
            key = "-".join(market.ticker.split("-")[:2])
            if markets_dict.get(key):
                pass
            else:
                markets_dict[key] = []
            markets_dict[key].append(market)

    # print(markets_dict)

    return markets_dict  # [market for market in markets if isinstance(market, ActiveMarket)]
