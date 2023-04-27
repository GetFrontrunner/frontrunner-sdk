from dataclasses import dataclass
from typing import Optional

class Prices:
    buy_for: Optional[float]=None
    buy_against: Optional[float]=None
    sell_for:Optional[float]=None
    sell_against:Optional[float]=None


class Quantities:
    buy_for: Optional[float]=None
    buy_against: Optional[float]=None
    sell_for:Optional[float]=None
    sell_against:Optional[float]=None


class Position:
    buy_for:Optional[int]=None
    buy_against:Optional[int]None
