from dataclasses import dataclass


@dataclass
class CancelOrder:
  market_id: str
  order_hash: str
  subaccount_index: int = 0
