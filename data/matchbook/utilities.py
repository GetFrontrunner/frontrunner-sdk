from typing import List, Dict, Any


class Country:
    def __init__(self, country_id: int, name: str, country_code: str):
        self.country_id = country_id
        self.name = name
        self.country_code = country_code


class Region:
    def __init__(self, region_id: int, name: str):
        self.region_id = region_id
        self.name = name


class Currency:
    def __init__(self, country_id: int, short_name: str, long_name: str):
        self.country_id = country_id
        self.short_name = short_name
        self.long_name = long_name


class Sport:
    def __init__(self, data):
        self.name = data.get("name", None)
        self.type = data.get("sport_type", None)
        self.id = data.get("sport_id", None)


class Price:
    def __init__(
        self,
        data,
    ):
        self.available_amount = data.get("available_amount", None)
        self.current = data.get("current", None)
        self.odds_type = data.get("odds_type", None)
        self.odds = data.get("odds", None)
        self.decimal_odds = data.get("decimal_odds", None)
        self.side = data.get("side", None)
        self.exchange_type = data.get("exchange_type", None)


class Prices:
    def __init__(self, data):
        self.prices = [Price(price) for price in data.get("prices", None)]


class Runner:
    def __init__(
        self,
        data,
    ):
        self.withdrawn = data.get("withdrawn", None)
        self.prices = [Price(price) for price in data.get("prices")]
        self.event_id = data.get("event_id", None)
        self.id = data.get("runner_id", None)
        self.market_id = data.get("market_id", None)
        self.name = data.get("name", None)
        self.status = data.get("status", None)
        self.volume = data.get("volume", None)
        self.event_participant_id = data.get("event_participant_id", None)


class Runners:
    def __init__(self, data):
        self.runners = [Runner(runner) for runner in data.get("runners", None)]


class Market:
    def __init__(self, data):
        self.event_id = data.get("event_id", None)
        self.market_id = data.get(" market_id", None)
        self.name = data.get("name", None)
        self.runners = [Runner(runner) for runner in data.get("runners", None)]


class Markets:
    def __init__(self, data):
        self.marekts = [Market(market) for market in data.get("marekts", None)]


class MetaTag:
    def __init__(self, data):
        self.meta_id = data.get("meta_id", None)
        self.name = data.get("name", None)
        self.meta_type = data.get("meta_type", None)
        self.url_name = data.get("url_name", None)


class Event:
    def __init__(self, data):
        self.id = data.get("event_id", None)
        self.name = data.get("name", None)
        self.sport_id = data.get("sport_id", None)
        self.start = data.get("start", None)
        self.in_running_flag = data.get("in_running_flag", None)
        self.allow_live_betting = data.get("allow_live_betting", None)
        self.category_id = data.get("category_id", None)
        self.status = data.get("status", None)
        self.volume = data.get("volume", None)
        self.markets = [Market(market) for market in data.get("markets", None)]
        self.meta_tags = [MetaTag(meta) for meta in data.get("meta_tags", None)]


class Events:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = [Event(event) for event in events]
