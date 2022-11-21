from requests import get
from typing import List, Union, Dict
from utils.markets import (
    Market,
    ActiveMarket,
    StagingMarket,
    MultiStatesMarket,
    binary_states_market_factory,
    multi_states_markets_factory,
)


def _get_all_markets(
    disable_error_msg: bool = False,
) -> List[Union[Market, None, MultiStatesMarket]]:
    resp = get("https://k8s.testnet.lcd.injective.network/injective/exchange/v1beta1/binary_options/markets")
    data = resp.json()
    markets = data["markets"]
    two_states_markets = [
        binary_states_market_factory(disable_error_msg, **market)
        for market in markets
        if binary_states_market_factory(disable_error_msg, **market)
    ]
    multi_states_markets = multi_states_markets_factory(markets)
    all_markets = multi_states_markets + two_states_markets
    return all_markets


def get_all_active_markets(
    disable_error_msg: bool = False,
) -> Dict[str, List[ActiveMarket]]:
    markets = _get_all_markets(disable_error_msg)
    tmp_markets_dict = {}
    for market in markets:
        if market and (isinstance(market, ActiveMarket) or isinstance(market, MultiStatesMarket)) and market.ticker:
            key = "-".join(market.ticker.split("-")[:2])
            if tmp_markets_dict.get(key):
                pass
            else:
                tmp_markets_dict[key] = []
            tmp_markets_dict[key].append(market)

    # print(markets_dict)
    markets_dict = {key: tmp_markets_dict[key] for key in sorted(tmp_markets_dict)}

    return markets_dict


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


if __name__ == "__main__":
    markets = get_all_active_markets()
    for market in markets:
        print(market)
