from typing import List, Union, Optional
from datetime import datetime
import numpy as np


class BetRadarResponseData:
    def __init__(self, data):
        self.data = data


class Error(BetRadarResponseData):
    def __init__(self, error):
        super().__init__(error)


class Markets:
    def __init__(self, data):
        if not data:
            data = {}
        self.respose_code = data.get("@respose_code", None)
        self.markets = [Market(market) for market in data.get("market", {})]
        # super().__init__(data)


class Market:
    def __init__(self, data):
        if not data:
            data = {}
        self.groups = data.get("@groups", None)
        self.id = data.get("@id", None)
        self.name = data.get("@name", None)
        self.variants = data.get("@variants", None)
        self.mappings = [Mapping(mapping) for mapping in data.get("@mappings", {}).get("mapping", {})]
        self.outcomes = [Outcome(outcome) for outcome in data.get("@outcomes", {}).get("outcome", {})]
        self.specifiers = [Specifier(specifier) for specifier in data.get("specifiers", {}).get("specifier", {})]


class Mapping:
    def __init__(self, data):
        if not data:
            data = {}

        self.market_id = data.get("@market_id", None)
        self.product_id = data.get("@product_id", None)
        self.product_ids = data.get("@product_ids", None)
        self.sov_template = data.get("@sov_template", None)
        self.sport_id = data.get("@sport_id", None)
        self.valid_for = data.get("@valid_for", None)
        self.mapping_outcome = [MappingOutcome(mapping_outcome) for mapping_outcome in data.get("mapping_outcome", [])]


class MappingOutcome:
    def __init__(self, data):
        if not data:
            data = {}

        self.outcome_id = data.get("@outcome_id", None)
        self.product_outcome_id = data.get("@product_outcome_id", None)
        self.product_outcome_name = data.get("@product_outcome_name", None)


class Outcome:
    def __init__(self, data):
        if not data:
            data = {}
        self.id = data.get("id")
        self.odds = data.get("odds")
        self.probabilities = data.get("probabilities")
        self.active = data.get("active")


class Specifier:
    def __init__(self, data):
        if not data:
            data = {}


class VoidReasons:
    def __init__(self, data):
        if not data:
            data = {}
        self.response_code = data.get("@response_code", None)
        self.void_reasons = [Reason(reason) for reason in data.get("void_reasons", [])]


class Reason:
    def __init__(self, data):
        if not data:
            data = {}
        self.description = data.get("@description", None)
        self.id = data.get("@id", None)


class BetStopReasons:
    def __init__(self, data):
        if not data:
            data = {}
        self.response_code = data.get("@response_code", None)

        self.bet_stop_reasons = [Reason(bet_stop_reason) for bet_stop_reason in data.get("betstop_reason", [])]


class BettingStatus:
    def __init__(self, data):
        if not data:
            data = {}

        self.response_code = data.get("@response_code", None)
        self.betting_status = [
            BStatus(betting_status)
            for betting_status in data.get("betting_status_description", {}).get("betting_status", [])
        ]


class BStatus:
    def __init__(self, data):
        self.description = data.get("@description", None)
        self.id = data.get("@id", None)


class MatchStatus:
    def __init__(self, data):
        if not data:
            data = {}
        self.response_code = data.get("@response_code", None)
        self.match_status = [data.get("@match_status_description", {}).get("match_status", {})]


class Mstatus:
    def __init__(self, data):
        if not data:
            data = {}
        self.description = data.get("@description", None)
        self.id = data.get("@id", None)
        self.period_number = data.get("@period_number", None)
        self.is_all_sports = data.get("@all", None)
        self.sports = [Sport(sport) for sport in data.get("sports", {}).get("sport", [])]


class RecoveryOdds(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class RecoveryEvent(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)
        pass


class RecoveryStateMessage(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)
        pass


class BookingCalendar(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)
        pass


class Fixture:
    def __init__(self, data):
        self.id = data.get("@id", None)
        self.next_live_time = data.get("@next_live_time", None)
        self.scheduled = Schedules(data)
        self.start_time = data.get("@start_time", None)
        self.start_time_confimed = data.get("@start_time_confimed", None)
        self.start_time_tbd = data.get("@start_time_tbd", None)
        self.status = data.get("@status", None)
        self.competitors = [Competitor(competitor) for competitor in data.get("competitors", {})]
        self.extra_info = [ExtraInfo(extra_info) for extra_info in data.get("extra_info", {}).get("info", [])]
        self.product_info = data.get("product_info", None)
        self.reference_ids = [
            ReferenceId(reference_id) for reference_id in data.get("reference_ids", {}).get("reference_id", {})
        ]
        self.season = Season(data.get("season", {}))
        self.tournament = Tournament(data.get("@tournament", {}))
        self.tournament_round = TournamentRound(data.get("@tournament_round", {}))
        self.tv_channels = data.get("@tv_channels", None)


class ExtraInfo:
    def __init__(self, data):
        self.key = data.get("@key")
        self.value = data.get("@value")


class Schedules:
    def __init__(self, data):
        if data:
            self.time = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")


class FixtureChanges(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class AllFixtureChanges(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Sports(BetRadarResponseData):
    def __init__(self, data):
        if data:
            sports_data = data.get("sports", None)
            sports = sports_data.get("sport", None) if sports_data else None
            if sports:
                self.sports = [Sport(sport) for sport in sports]


class Sport:
    def __init__(self, data):
        self.sport_id = data["@id"]
        self.name = data["@name"]


class Tournaments:
    def __init__(self, data):
        if not data:
            data = {}
        tournaments_data = data.get("sport_tournaments", {})
        sport_data = tournaments_data.get("sport", None)
        self.sport = Sport(sport_data)

        tournaments = tournaments_data.get("tournaments", {})
        tournament = tournaments.get("tournament", [])
        self.tournaments = [Tournament(t) for t in tournament]


class Tournament:
    def __init__(self, data):
        self.id = data.get("@id", None)
        self.name = data.get("name", None)
        self.sport = Sport(data.get("sport", None))
        self.category = Category(data.get("category", None))
        self.current_season = Season(data.get("current_season", None))
        self.scheduled = Schedules(data.get("@scheduled", None))
        self.scheduled_end = Schedules(data.get("@scheduled_end", None))


class Seasons:
    def __init__(self, data):
        if not data:
            data = {}
        seasons_data = data.get("seasons", {})
        self.seasons = [Season(season) for season in seasons_data.get("season", [])]
        self.tournament = Tournament(data.get("@tournament", None))


class Variants:
    def __init__(self, data):
        if not data:
            data = {}
        self.response_code = data.get("variant_desciptions", {}).get("@response_code", None)
        self.variants = data.get("variant_desciptions", {}).get("variants", [])


class Variant:
    def __init__(self, data):
        if not data:
            data = {}
        self.id = data.get("@id", {})
        self.outcomes = [Outcome(outcome) for outcome in data.get("outcomes", {}).get("outcome", [])]
        self.mappings = [Mapping(mapping) for mapping in data.get("mappings", {}).get("mapping", [])]


class Producers:
    def __init__(self, data):
        if not data:
            data = {}
        self.producers = [Producer(producer) for producer in data.get("producers", {}).get("producer", [])]


class Producer:
    def __init__(self, data):
        if not data:
            data = {}

        self.id = data.get("@id", None)
        self.name = data.get("@name", None)
        self.description = data.get("@description", None)
        self.api_url = data.get("@api_url", None)
        self.active = data.get("@active", None)
        self.scope = data.get("@scope", None)
        self.stateful_recovery_window_in_minutes = data.get("@stateful_recovery_window_in_minutes", None)


class Status(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Reasons(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Players(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Player(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Competitors(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Venues(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Description(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Probability(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Probabilities:
    def __init__(self, data, n):
        if not data:
            prob = np.random.random()
            odds = prob / (1 - prob)
            event_1 = {"id": n, "odds": odds, "probabilities": prob, "active": 1}

            prob = 1 - prob
            odds = prob / (1 - prob)
            event_2 = {"id": n, "odds": odds, "probabilities": prob, "active": 1}

            self.outcomes = [Outcome(event_1), Outcome(event_2)]


# <odds>
#    <market status="0" id="16" specifiers="hcp=-1" extended_specifiers="hcp_for_the_rest=-1"/>
#    <market status="0" id="16" specifiers="hcp=0.75" extended_specifiers="hcp_for_the_rest=0.75"/>
#    <market status="1" id="18" specifiers="total=3.5" extended_specifiers="total_for_the_rest=3.5">
#      <outcome id="12" odds="3.55" probabilities="0.2319363847" active="1"/>
#      <outcome id="13" odds="1.22" probabilities="0.7680636153" active="1"/>
#
class AvailableSelection(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class User(BetRadarResponseData):
    def __init__(self, data):
        bookmaker_details = data.get("bookmaker_details", None)
        if bookmaker_details:
            expire_at = bookmaker_details.get("@expire_at", None)
            self.expire_at = datetime.strptime(expire_at, "%Y-%m-%dT%H:%M:%SZ") if expire_at else None
            self.bookmaker_id = int(bookmaker_details.get("@bookmaker_id", None))
            self.virtual_host = bookmaker_details.get("@virtual_host", None)


class Info:
    def __init__(self, data):
        tournment_info = data.get("tournment_info", {})
        self.live_coverage = tournment_info.get("coverage_info", {}).get("@live_coverage", None)
        self.groups = [
            Competitor(competitor)
            for competitor in tournment_info.get("groups", {}).get("group", {}).get("competitor", [])
        ]
        self.round = Round(tournment_info.get("round", {}))
        self.season = Season(tournment_info.get("season", {}))
        self.tournament = Tournament(tournment_info.get("tournament", {}))


class Round:
    def __init__(self, data):
        if not data:
            data = {}
        self.number = data.get("@number", None)
        self.type = data.get("@type", None)


class Categories:
    def __init__(self, data):
        sport_categories_data = data.get("sport_categories", None)
        self.sport = None
        self.categories = None
        if sport_categories_data:
            if sport_categories_data["sport"]:
                self.sport = sport_categories_data.get("sport", None)
            if sport_categories_data.get("categories", None) and sport_categories_data.get("categories", None).get(
                "category", None
            ):
                self.categories = [
                    Category(category)
                    for category in sport_categories_data.get("categories", None).get("category", None)
                ]


class Category:
    def __init__(self, data):
        self.id = data.get("@id", None)
        self.name = data.get("@name", None)
        self.country_code = data.get("@country_code", None)


class Events(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Timeline:
    def __init__(self, data):
        if not data:
            data = {}

        # self.generate_at = datetime.strptime(
        #    data.get("@generate_at", None), "%Y-%m-%dT%H:%M:%SZ"
        # )
        self.sport_event = SportEvent(data.get("sport_event", None))
        self.sport_event_conditions = data.get("sport_event_conditions", None)
        self.sport_event_status = SportEventStatus(data.get("sport_event_status", None))


class SportEvent:
    def __init__(self, data):
        if not data:
            data = {}
        self.id = data.get("@id", None)
        self.scheduled = (
            datetime.strptime(data.get("@scheduled", None), "%Y-%m-%dT%H:%M:%SZ")
            if data.get("@scheduled", None)
            else None
        )
        self.start_time_tbd = data.get("@start_time_tbd", None)
        competitors_data = data.get("competitors", None)
        if not competitors_data:
            competitors_data = {}

        self.competitors = [Competitor(competitor) for competitor in competitors_data.get("competitor", [])]

        self.season = Season(data.get("@season", None))

        self.tournament = Tournament(data.get("@tournament", None))

        self.tournament_round = TournamentRound(data.get("@tournament_round", None))


class Competitor:
    def __init__(self, data):
        if not data:
            data = {}
        self.abbreviation = data.get("@abbreviation", None)
        self.country = data.get("@country", None)
        self.country_code = data.get("@country_code", None)
        self.gender = data.get("@gender", None)
        self.id = data.get("@id", None)
        self.name = data.get("@name", None)
        self.qualifier = data.get("@qualifier", None)
        self.reference_ids = ReferenceId(data.get("@reference_ids", None))


class ReferenceId:
    def __init__(self, data: Optional[dict]):
        if not data:
            data = {}
        self.name = data.get("@name", None)
        self.value = data.get("@value", None)


class Season:
    def __init__(self, data):
        if not data:
            data = {}
        self.end_date = data.get("@end_date", None)
        self.id = data.get("@id", None)
        self.name = data.get("@name", None)
        self.start_date = data.get("start_date", None)
        self.tournament_id = data.get("tournament_id", None)
        self.year = data.get("@year", None)


class TournamentRound:
    def __init__(self, data):
        if not data:
            data = {}
        self.betradar_id = data.get("@betradar_id", None)
        self.betradar_name = data.get("@betradar_name", None)
        self.group_long_name = data.get("@group_long_name", None)
        self.number = data.get("@number", None)
        self.type = data.get("@type", None)


class SportEventStatus:
    def __init__(self, data):
        if not data:
            data = {}
        self.away_score = data.get("@away_score", None)
        self.home_score = data.get("@home_score", None)
        self.match_status = data.get("@match_status", None)
        self.match_status_code = data.get("@match_status_code", None)
        self.status = data.get("@status", None)
        self.status_code = data.get("@status_code", None)

        period_scores_data = data.get("period_scores", None)
        if not period_scores_data:
            period_scores_data = {}
        self.period_scores = [PeriodScore(period_score) for period_score in period_scores_data.get("period_score", [])]

        results_data = data.get("results", None)
        if not results_data:
            results_data = {}
        self.results = [Result(result) for result in results_data.get("result", [])]


class PeriodScore:
    def __init__(self, data):
        if not data:
            data = {}
        self.away_score = data.get("@away_score", None)
        self.home_score = data.get("@home_score", None)
        self.match_status_code = data.get("@match_status_code", None)
        self.number = data.get("@number", None)
        self.type = data.get("@type", None)
        pass


class Result:
    def __init__(self, data):
        if not data:
            data = {}
        self.away_score = data.get("@away_score", None)
        self.home_score = data.get("@home_score", None)
        self.match_status = data.get("@match_status", None)


class Summary:
    def __init__(self, data):
        if not data:
            data = {}
        # self.generate_at = datetime.strptime(
        #    data.get("@generate_at", None), "%Y-%m-%dT%H:%M:%SZ"
        # )
        self.sport_event = SportEvent(data.get("sport_event", None))
        self.sport_event_conditions = data.get("sport_event_conditions", None)
        self.sport_event_status = SportEventStatus(data.get("sport_event_status", None))


class Summaries:
    def __init__(self, data):
        pass
