from datetime import datetime
from time import time
import logging


def factory(disable_error_msg: bool = False, **kwargs):
    if kwargs.get("ticker"):
        ticker = kwargs["ticker"]
        if len(ticker.split("-")) == 3:
            return ActiveMarket(
                ticker=kwargs.get("ticker"),  # "staging-1659438300-NYM-WSH"
                oracle_symbol=kwargs.get("oracle_symbol"),  # "Frontrunner"
                oracle_provider=kwargs.get("oracle_provider"),  # "Frontrunner"
                oracle_type=kwargs.get("oracle_type"),  # "Provider"
                oracle_scale_factor=kwargs.get("oracle_scale_factor"),  # 6
                expiration_timestamp=kwargs.get("expiration_timestamp"),  # "1659438300"
                settlement_timestamp=kwargs.get("settlement_timestamp"),  # "1659481500"
                admin=kwargs.get("admin"),  # "inj1v0txc0ep93a3xsxlcf36ctwh3uhxzjackcctp3"
                quote_denom=kwargs.get("quote_denom"),  # "peggy0x87aB3B4C8661e07D6372361211B96ed4Dc36B1B5"
                market_type=kwargs.get("market_type"),
                market_id=kwargs.get("market_id"),
                maker_fee_rate=kwargs.get("maker_fee_rate"),  # "0.000000000000000000"
                taker_fee_rate=kwargs.get("taker_fee_rate"),  # "0.000000000000000000"
                relayer_fee_share_rate=kwargs.get("relayer_fee_share_rate"),
                # "0.400000000000000000"
                status=kwargs.get("status"),  # "Active"
                min_price_tick_size=kwargs.get("min_price_tick_size"),
                # "10000.000000000000000000"
                min_quantity_tick_size=kwargs.get("min_quantity_tick_size"),
                # "1.000000000000000000"
                settlement_price=kwargs.get("settlement_price"),  # None
            )
        elif "staging" in ticker:
            return StagingMarket(
                ticker=kwargs.get("ticker"),  # "staging-1659438300-NYM-WSH"
                oracle_symbol=kwargs.get("oracle_symbol"),  # "Frontrunner"
                oracle_provider=kwargs.get("oracle_provider"),  # "Frontrunner"
                oracle_type=kwargs.get("oracle_type"),  # "Provider"
                oracle_scale_factor=kwargs.get("oracle_scale_factor"),  # 6
                expiration_timestamp=kwargs.get("expiration_timestamp"),  # "1659438300"
                settlement_timestamp=kwargs.get("settlement_timestamp"),  # "1659481500"
                admin=kwargs.get("admin"),  # "inj1v0txc0ep93a3xsxlcf36ctwh3uhxzjackcctp3"
                quote_denom=kwargs.get("quote_denom"),  # "peggy0x87aB3B4C8661e07D6372361211B96ed4Dc36B1B5"
                market_type=kwargs.get("market_type"),
                market_id=kwargs.get("market_id"),
                maker_fee_rate=kwargs.get("maker_fee_rate"),  # "0.000000000000000000"
                taker_fee_rate=kwargs.get("taker_fee_rate"),  # "0.000000000000000000"
                relayer_fee_share_rate=kwargs.get("relayer_fee_share_rate"),
                # "0.400000000000000000"
                status=kwargs.get("status"),  # "Active"
                min_price_tick_size=kwargs.get("min_price_tick_size"),
                # "10000.000000000000000000"
                min_quantity_tick_size=kwargs.get("min_quantity_tick_size"),
                # "1.000000000000000000"
                settlement_price=kwargs.get("settlement_price"),  # None
            )
        else:
            if disable_error_msg:
                pass
            else:
                logging.warn(f"Unknown type of market: {kwargs.get('ticker')}")
            # raise Exception("Unknown type of market")
            return None
    else:
        raise Exception("No market")


class Market:
    def __init__(self, **kwargs):
        self.ticker = kwargs.get("ticker")  # "staging-1659438300-NYM-WSH"
        self.oracle_symbol = kwargs.get("oracle_symbol")  # "Frontrunner"
        self.oracle_provider = kwargs.get("oracle_provider")  # "Frontrunner"
        self.oracle_type = kwargs.get("oracle_type")  # "Provider"
        self.oracle_scale_factor = kwargs.get("oracle_scale_factor")  # 6
        self.expiration_timestamp = kwargs.get("expiration_timestamp")
        # "1659438300"
        self.settlement_timestamp = kwargs.get("settlement_timestamp")
        # "1659481500"
        self.admin = kwargs.get("admin")
        # "inj1v0txc0ep93a3xsxlcf36ctwh3uhxzjackcctp3"
        self.quote_denom = kwargs.get("quote_denom")
        # "peggy0x87aB3B4C8661e07D6372361211B96ed4Dc36B1B5"
        self.market_type = kwargs.get("market_type")
        self.market_id = kwargs.get("market_id")
        self.maker_fee_rate = kwargs.get("maker_fee_rate")  # "0.000000000000000000"
        self.taker_fee_rate = kwargs.get("taker_fee_rate")  # "0.000000000000000000"
        self.relayer_fee_share_rate = kwargs.get("relayer_fee_share_rate")
        self.status = kwargs.get("status")  # "Active"
        self.min_price_tick_size = kwargs.get("min_price_tick_size")
        self.min_quantity_tick_size = kwargs.get("min_quantity_tick_size")
        self.settlement_price = kwargs.get("settlement_price")  # None

    def deactive_market(self):
        self.market_type = "deactived"

    def activate_market(self):
        self.market_type = "activate"


class ActiveMarket(Market):
    """
    Tradable market
    """


class StagingMarket(Market):
    """
    Staging market
    """


if __name__ == "__main__":
    import json

    with open("./markets.json", "r") as file:
        data = file.read()
    obj = json.loads(data)
    for market in obj["markets"]:
        pass
    print(obj["markets"][0])
