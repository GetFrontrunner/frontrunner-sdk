from typing import List, Union, Optional
from time import time_ns
from math import log
import logging
from aiohttp import ClientTimeout, TCPConnector, ClientSession
from asyncio import sleep

from pickle import dumps

from utils.utilities import RedisProducer

from data.betradar.utilities import *


class Data:
    def __init__(self, data):
        self.data = data


class RecoveryOdds(Data):
    def __init__(self, data):
        super().__init__(data)


class RecoveryEvent(Data):
    def __init__(self, data):
        super().__init__(data)


class RecoveryStateMessage(Data):
    def __init__(self, data):
        super().__init__(data)


class BookingCalendar(Data):
    def __init__(self, data):
        super().__init__(data)


class Fixture(Data):
    def __init__(self, data):
        super().__init__(data)


class Schedules(Data):
    def __init__(self, data):
        super().__init__(data)


class FixtureChanges(Data):
    def __init__(self, data):
        super().__init__(data)


class Summary(Data):
    def __init__(self, data):
        super().__init__(data)


class Timeline(Data):
    def __init__(self, data):
        super().__init__(data)


class Sports(Data):
    def __init__(self, data):
        super().__init__(data)


class Tournaments:
    def __init__(self, data):
        pass


class Tournament(Data):
    def __init__(self, data):
        super().__init__(data)


class Seasons(Data):
    def __init__(self, data):
        super().__init__(data)


class Players(Data):
    def __init__(self, data):
        super().__init__(data)


class Competitors(Data):
    def __init__(self, data):
        super().__init__(data)


class Venues(Data):
    def __init__(self, data):
        super().__init__(data)


class Description(Data):
    def __init__(self, data):
        super().__init__(data)


class Probabilities(Data):
    def __init__(self, data):
        super().__init__(data)


class User(Data):
    def __init__(self, data):
        super().__init__(data)
