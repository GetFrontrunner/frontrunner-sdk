from typing import List, Dict, Any, Optional
from datetime import datetime


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
        self.type = data.get("type", None)
        self.id = data.get("id", None)


class Price:
    def __init__(
        self,
        data,
    ):
        self.available_amount = data.get("available-amount", None)
        self.currency = data.get("currency", None)
        self.odds_type = data.get("odds-type", None)
        self.odds = data.get("odds", None)
        self.decimal_odds = data.get("decimal-odds", None)
        self.side = data.get("side", None)
        self.exchange_type = data.get("exchange-type", None)


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
        self.event_id = data.get("event-id", None)
        self.id = data.get("id", None)
        self.market_id = data.get("market-id", None)
        self.name = data.get("name", None)
        self.status = data.get("status", None)
        self.volume = data.get("volume", None)
        self.event_participant_id = data.get("event-participant-id", None)


class Runners:
    def __init__(self, data):
        self.runners = [Runner(runner) for runner in data.get("runners", None)]


class Market:
    def __init__(self, data):
        self.event_id = data.get("event-id", None)
        self.market_id = data.get(" market-id", None)
        self.name = data.get("name", None)
        self.runners = [Runner(runner) for runner in data.get("runners", None)]


class Markets:
    def __init__(self, data):
        self.marekts = [Market(market) for market in data.get("marekts", None)]


class MetaTag:
    def __init__(self, data):
        self.meta_id = data.get("id", None)
        self.name = data.get("name", None)
        self.meta_type = data.get("type", None)
        self.url_name = data.get("url-name", None)


class Event:
    def __init__(self, data):
        self.id: Optional[int] = data.get("id", None)
        self.name: Optional[str] = data.get("name", None)
        self.sport_id: Optional[int] = data.get("sport-id", None)
        if data.get("start", None):
            self.start: Optional[datetime] = datetime.strptime(
                data.get("start", None), "%Y-%m-%dT%H:%M:%S.%fZ"
            )
        else:
            self.start = None

        self.in_running_flag: Optional[bool] = data.get("in-running-flag", None)
        self.allow_live_betting: Optional[bool] = data.get("allow-live-betting", None)
        self.category_id: List[int] = data.get("category-id", None)
        self.status: Optional[str] = data.get("status", None)
        self.volume: Optional[int] = data.get("volume", None)
        if data.get("markets", None):
            self.markets = [Market(market) for market in data.get("markets", None)]
        else:
            self.markets = []

        if data.get("meta-tags", None):
            self.meta_tags = [MetaTag(meta) for meta in data.get("meta-tags", None)]
        else:
            self.meta_tags = []


class Events:
    def __init__(self, events: Dict[str, Any], in_running_flag: bool = True):
        if in_running_flag:
            self.events: List[Event] = [
                Event(event) for event in events["events"] if event["in-running-flag"]
            ]
        else:
            self.events: List[Event] = [Event(event) for event in events]
