from dataclasses import dataclass
from typing import Optional


@dataclass
class CancelOrder:
  market_id: str
  order_hash: Optional[str] = None
