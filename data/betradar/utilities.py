from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep
from pickle import dumps
from utils.utilities import RedisProducer


class BetRadarResponseData:
    def __init__(self, data):
        self.data = data


class Error(BetRadarResponseData):
    def __init__(self, error):
        super().__init__(error)


class Markets(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class RecoveryOdds(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class RecoveryEvent(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class RecoveryStateMessage(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class BookingCalendar(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Fixture(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Schedules(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class FixtureChanges(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class ResultsChanges(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Summary(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Timeline(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Sports(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Tournaments:
    def __init__(self, data):
        pass


class Tournament(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Seasons(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Variants(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Variant(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


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


class Probabilities(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class AvailableSelection(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class User(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Info(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Categories(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Events(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class Summaries(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)
