class PreGameOdds:
    def __init__(self, data):
        self.markets = [MarketOdds(d) for d in data]


class InGameOdds:
    def __init__(self, data):
        self.markets = [MarketOdds(d) for d in data]


class MarketOdds:
    def __init__(self, data):
        self.ScoreId = data["ScoreId"]  # 18206,
        self.Season = data["Season"]  # 2022,
        self.SeasonType = data["SeasonType"]  # 1,
        self.Week = data["Week"]  # 15,
        self.Day = data["Day"]  # "2022-12-15T00:00:00",
        self.DateTime = data["DateTime"]  # "2022-12-15T20:15:00",
        self.Status = data["Status"]  # "Final",
        self.AwayTeamId = data["AwayTeamId"]  # 31,
        self.HomeTeamId = data["HomeTeamId"]  # 30,
        self.AwayTeamName = data["AwayTeamName"]  # "SF",
        self.HomeTeamName = data["HomeTeamName"]  # "SEA",
        self.GlobalGameId = data["GlobalGameId"]  # 18206,
        self.GlobalAwayTeamId = data["GlobalAwayTeamId"]  # 31,
        self.GlobalHomeTeamId = data["GlobalHomeTeamId"]  # 30,
        self.HomeTeamScore = data["HomeTeamScore"]  # 13,
        self.AwayTeamScore = data["AwayTeamScore"]  # 21,
        self.TotalScore = data["TotalScore"]  # 34,
        self.HomeRotationNumber = data["HomeRotationNumber"]  # 302,
        self.AwayRotationNumber = data["AwayRotationNumber"]  # 301,
        self.PregameOdds = [Odds(odds) for odds in data["PregameOdds"]]  # [],
        self.LiveOdds = [Odds(odds) for odds in data["LiveOdds"]]  # []
        self.AlternateMarketPregameOdds = data["AlternateMarketPregameOdds"]  # [],


class Odds:
    def __init__(self, data):
        self.GameOddId = data["GameOddId"]  #: 2620284,
        self.Sportsbook = data["Sportsbook"]  #: "DraftKings",
        self.ScoreId = data["ScoreId"]  #: 18206,
        self.Created = data["Created"]  #: "2022-12-15T23:12:45",
        self.Updated = data["Updated"]  #: "2022-12-15T23:16:35",
        self.HomeMoneyLine = data["HomeMoneyLine"]  #: 2200,
        self.AwayMoneyLine = data["AwayMoneyLine"]  #: -17500,
        self.DrawMoneyLine = data["DrawMoneyLine"]  #: None,
        self.HomePointSpread = data["HomePointSpread"]  #: 7.5,
        self.AwayPointSpread = data["AwayPointSpread"]  #: -7.5,
        self.HomePointSpreadPayout = data["HomePointSpreadPayout"]  #: 1000,
        self.AwayPointSpreadPayout = data["AwayPointSpreadPayout"]  #: -2100,
        self.OverUnder = data["OverUnder"]  #: None,
        self.OverPayout = data["OverPayout"]  #: None,
        self.UnderPayout = data["UnderPayout"]  #: None,
        self.SportbookId = data["SportsbookId"]  #: 7,
        self.OddType = data["OddType"]  #: "live",
        self.SportsbookUrl = data["SportsbookUrl"]  # None,
