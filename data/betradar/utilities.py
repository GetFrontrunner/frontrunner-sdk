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


class Players(BetRadarResponseData):
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


class Probabilities(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)


class User(BetRadarResponseData):
    def __init__(self, data):
        super().__init__(data)
