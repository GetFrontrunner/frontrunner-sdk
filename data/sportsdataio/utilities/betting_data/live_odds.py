from typing import Dict, List


class BettingType:
    def __init__(self, data: Dict[str, str]):
        self.record_id = data.get("RecordId")
        self.name = data.get("name")


class BettingTypes:
    def __init__(self, data: List[Dict[str, str]]):
        self.types = [BettingType(type_data) for type_data in data]


class BettingMarketMetaData:
    def __init__(self, data: Dict[str, str]):
        self.betting_market_type_id = data.get("BettingMarketTypeId")
        self.betting_bet_type_id = data.get("BettingBetTypeId")
        self.betting_period_type_id = data.get("BettingPeriodTypeId")


class BettingMetaData:
    def __init__(self, data: Dict[str, List[Dict[str, str]]]):
        self.betting_bet_types = [
            BettingType(betting_bet_type)
            for betting_bet_type in data.get("BettingBetTypes", [])
        ]
        self.betting_market_types = [
            BettingType(betting_market_type)
            for betting_market_type in data.get("BettingMarketTypes", [])
        ]
        self.betting_bet_types = [
            BettingType(betting_period_type)
            for betting_period_type in data.get("BettingPeriodTypes", [])
        ]
        self.betting_bet_types = [
            BettingType(betting_event_type)
            for betting_event_type in data.get("BettingEventTypes", [])
        ]
        self.betting_bet_types = [
            BettingType(betting_outcome_type)
            for betting_outcome_type in data.get("BettingOutcomeTypes", [])
        ]
        self.betting_bet_types = [
            BettingType(betting_result_type)
            for betting_result_type in data.get("BettingResultTypes", [])
        ]
        self.betting_bet_types = [
            BettingType(market_meta_data)
            for market_meta_data in data.get("ResultedMarketMetaData", [])
        ]


class BettingEventByDate:
    def __init__(self, data: Dict[str, str]):
        self.betting_event_id = data.get("BettingEventID")
        self.name = data.get("Name")
        self.season = data.get("Season")
        self.betting_event_type_id = data.get("BettingEventTypeID")
        self.betting_event_type = data.get("BettingEventType")
        self.start_date = data.get("StartDate")
        self.created = data.get("Created")
        self.updated = data.get("Updated")
        self.game_id = data.get("GameID")
        self.global_game_id = data.get("GlobalGameID")
        self.game_status = data.get("GameStatus")
        self.quarter = data.get("Quarter")
        self.away_team = data.get("AwayTeam")
        self.home_team = data.get("HomeTeam")
        self.away_team_id = data.get("AwayTeamID")
        self.home_team_id = data.get("HomeTeamID")
        self.global_away_team_id = data.get("GlobalAwayTeamID")
        self.global_home_team_id = data.get("GlobalHomeTeamID")
        self.away_team_score = data.get("AwayTeamScore")
        self.home_team_score = data.get("HomeTeamScore")
        self.total_score = data.get("TotalScore")
        self.away_rotation_number = data.get("AwayRotationNumber")
        self.home_rotation_number = data.get("HomeRotationNumber")
        self.game_start_time = data.get("GameStartTime")
        self.betting_markets = data.get("BettingMarkets")


class BettingMarket:
    def __init__(self, data: Dict):
        self.betting_market_id = data.get("BettingMarketID")  #: 63182,
        self.betting_event_id = data.get("BettingEventID")
        self.betting_market_type_id = data.get("BettingMarketTypeID")
        self.betting_market_type = data.get("BettingMarketType")
        self.betting_bet_type_id = data.get("BettingBetTypeID")
        self.betting_bet_type = data.get("BettingBetType")
        self.betting_period_type_id = data.get("BettingPeriodTypeID")
        self.betting_period_type = data.get("BettingPeriodType")
        self.name = data.get("Name")
        self.team_id = data.get("TeamID")
        self.team_key = data.get("TeamKey")
        self.player_id = data.get("PlayerID")
        self.player_name = data.get("PlayerName")
        self.created = data.get("Created")
        self.updated = data.get("Updated")
        self.any_bets_available = data.get("AnyBetsAvailable")
        self.available_sportsbooks = [
            SportBook(sportbook) for sportbook in data.get("AvailableSportsbooks", [])
        ]
        self.betting_outcomes = data.get("BettingOutcomes")
        self.consensus_outcomes = data.get("ConsensusOutcomes")


class BettingFuture:
    def __init__(self, data):
        self.betting_event_id = data.get("BettingEventID")
        self.name = data.get("Name")
        self.season = data.get("Season")
        self.betting_event_type_id = data.get("BettingEventTypeID")
        self.betting_event_type = data.get("BettingEventType")
        self.start_date = data.get("StartDate")
        self.created = data.get("Created")
        self.updated = data.get("Updated")
        self.game_id = data.get("GameID")
        self.global_game_id = data.get("GlobalGameID")
        self.game_status = data.get("GameStatus")
        self.quarter = data.get("Quarter")
        self.away_team = data.get("AwayTeam")
        self.home_team = data.get("HomeTeam")
        self.away_team_id = data.get("AwayTeamID")
        self.home_team_id = data.get("HomeTeamID")
        self.global_away_team_id = data.get("GlobalAwayTeamID")
        self.global_home_team_id = data.get("GlobalHomeTeamID")
        self.away_team_score = data.get("AwayTeamScore")
        self.home_team_score = data.get("HomeTeamScore")
        self.total_score = data.get("TotalScore")
        self.away_rotation_number = data.get("AwayRotationNumber")
        self.home_rotation_number = data.get("HomeRotationNumber")
        self.game_start_time = data.get("GameStartTime")
        self.betting_markets = [
            BettingMarket(betting_market)
            for betting_market in data.get("BettingMarkets")
        ]


class SportBook:
    def __init__(self, data):
        self.sport_book_id = data.get("SportsbookID")
        self.name = data.get("Name")


class BettingFuturesBySeason:
    def __init__(self, data):
        self.betting_futures = [
            BettingFuture(betting_future) for betting_future in data
        ]


class Odds:
    def __init__(self, data):
        self.game_id = data.get("GameId")
        self.season = data.get("Season")
        self.season_type = data.get("SeasonType")
        self.day = data.get("Day")
        self.date_time = data.get("DateTime")
        self.status = data.get("Status")
        self.away_team_id = data.get("AwayTeamId")
        self.home_team_id = data.get("HomeTeamId")
        self.away_team_name = data.get("AwayTeamName")
        self.home_team_name = data.get("HomeTeamName")
        self.global_game_id = data.get("GlobalGameId")
        self.global_away_team_id = data.get("GlobalAwayTeamId")
        self.global_home_team_id = data.get("GlobalHomeTeamId")
        self.home_team_score = data.get("HomeTeamScore")
        self.away_team_score = data.get("AwayTeamScore")
        self.total_score = data.get("TotalScore")
        self.home_rotation_number = data.get("HomeRotationNumber")
        self.away_rotation_number = data.get("AwayRotationNumber")
        self.pregame_odds = data.get("PregameOdds")
        self.live_odds = data.get("LiveOdds")
        self.alternate_market_pregame_odds = data.get("AlternateMarketPregameOdds")


class InGameOdds:
    def __init__(self, data):
        self.odds = [Odds(odds) for odds in data]


class BettingEventsByDate:
    def __init__(self):
        pass


class InGameOddsByDate:
    def __init__(self, data):
        self.odds = [Odds(odds) for odds in data]


class InGameOddsLineMovement:
    def __init__(self, data):
        self.odds = [Odds(odds) for odds in data]
        pass


class PeriodGameOddsByDate:
    def __init__(self,data):
        pass


class PeriodGameOddsLineMovement:
    def __init__(self,data):
        pass


class PreGameOddsByDate:
    def __init__(self,data):
        self.odds = [Odds(odds) for odds in data]
        pass


class PreGameOddsLineMovement:
    def __init__(self,data):
        self.odds = [Odds(odds) for odds in data]
        pass


class SportsBooks:
    def __init__(self, data):
        pass
    
class SportBooks:
    def __init__(self,data):
        pass
