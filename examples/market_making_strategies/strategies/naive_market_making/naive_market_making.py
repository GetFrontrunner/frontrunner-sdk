"""
1. Reads list in the format below,
2. Processing a new sub-list every tickTimeSeconds
3. Canceling/re-creating corresponding orders as needed to create a spread of spreadSizeDollars
with order sizes of orderSizePerSide
"""

import asyncio
import json

from math import floor
from time import sleep
from typing import Dict
from typing import List
from typing import Tuple

from examples.market_making_strategies.core.market_maker import MarketMaker
from sortedcontainers import SortedKeyList

from frontrunner_sdk.models.cancel_order import CancelOrder
from frontrunner_sdk.models.order import Order


class NaiveMarketMaker(MarketMaker):

  def __init__(self, market_id: str, n_orders: int, tick_time_seconds: int):
    super().__init__(market_id=market_id, n_orders=n_orders)
    self.buy_for = SortedKeyList(key=lambda order: -int(order.price))
    self.buy_against = SortedKeyList(key=lambda order: int(order.price))
    self.spread_size_dollars = 0.04
    self.order_size_per_side = 10
    self.tick_time_seconds = tick_time_seconds

  def float_round_down(self, probability: float, decimal: int = 2) -> float:
    return floor(probability * (10**decimal)) / (10**decimal)

  def read_probability_data(self, data: Dict):
    self.order_size_per_side = int(data["orderSizePerSide"])
    self.spread_size_dollars = float(data["spreadSizeDollars"])
    self.tick_time_seconds = int(data["tickTimeSeconds"])
    prob_list = data["probabilitiesLists"]
    return [prob["longProbability"] for prob in prob_list if prob["injectiveMarketId"] == self.market_id]

  def _get_prices(self):
    pass

  def get_prices(self, probabilities: List[float]) -> Tuple[List[float], List[float]]:
    # TODO: maybe be its better with SortedList()
    buy_long_prices = []
    buy_short_prices = []

    for probability in probabilities:
      if probability < 1 - probability:
        buy_long_prices.append(self.float_round_down(probability + self.spread_size_dollars / 2))
        buy_short_prices.append(self.float_round_down(1 - probability - self.spread_size_dollars / 2))
      else:
        buy_long_prices.append(self.float_round_down(probability - self.spread_size_dollars / 2))
        buy_short_prices.append(self.float_round_down(1 - probability + self.spread_size_dollars / 2))
    buy_long_prices.sort()
    buy_short_prices.sort(reverse=True)
    return (buy_long_prices, buy_short_prices)

  def _get_quantities(self, prices: List[float], multiplier) -> List[int]:
    return [int(multiplier * price) for price in prices]

  def get_quantities(self, prices: Tuple[List[float], List[float]]) -> Tuple[List[int], List[int]]:
    buy_for_quantity = self._get_quantities(prices[0], self.order_size_per_side)
    buy_against_quantity = self._get_quantities(prices[1], self.order_size_per_side)
    return (buy_for_quantity, buy_against_quantity)

  def get_new_order(self, prices: Tuple[List[float], List[float]], quantities: Tuple[List[int],
                                                                                     List[int]]) -> List[Order]:
    buy_for = self.build_buy_orders(prices=prices[0], quantities=quantities[0], sides=["long" for _ in quantities])
    buy_against = self.build_buy_orders(prices=prices[1], quantities=quantities[1], sides=["short" for _ in quantities])
    return buy_for + buy_against

  def initilization(self):
    self.fund_wallet()

  def strategy(self):
    while True:
      sleep(self.tick_time_seconds)
      if (len(self.buy_for) != 0):
        self.buy_for.clear()
      if (len(self.buy_against) != 0):
        self.buy_against.clear()

      # in here, we read this file very n seconds
      json_file = open("examples/market_making_strategies/data/probabilities.json")
      probabilities_data = json.load(json_file)
      probabilities = self.read_probability_data(probabilities_data)
      prices = self.get_prices(probabilities)
      quantities = self.get_quantities(prices)
      new_orders = self.get_new_order(prices, quantities)

      #  get the old orders, we will cancel them after we send new orders
      #  TODO: ideally we send a new order, and cancel an old order
      #  this can be done in batch order, meaning both new order and cancel order happens in same block,
      #  but I can't find it
      orders_to_cancel = asyncio.run(self.get_my_orders())
      asyncio.run(self.create_orders(new_orders))

      # we canel the outdated orders, because we have sent the new orders to chain.
      # Cancel outdated orders now will not leave orderbook empty
      old_orders_to_cacnel = [
        CancelOrder(market_id=self.market_id, order_hash=order.order_hash) for order in orders_to_cancel.orders
      ]

      if old_orders_to_cacnel:
        asyncio.run(self.cancel_orders(old_orders_to_cacnel))

      # Check the total number of orders in each side of orderbook
      open_orders = asyncio.run(self.get_my_orders())
      for order in open_orders.orders:
        if order.order_side == "buy":
          self.buy_for.add(order)
        else:
          self.buy_against.add(order)

      new_buy_for_prices = []
      new_buy_against_prices = []
      new_buy_for_quantities = []
      new_buy_against_quantities = []

      new_cancel_orders = []
      # check for missing order, or uncancelled old orders
      if (len(self.buy_for) != self.n_orders):
        if len(self.buy_for) < self.n_orders:
          for i in range(len(self.buy_for), self.n_orders):
            # FIXME not good
            new_buy_for_prices.append(prices[0][i])
            new_buy_for_quantities = self._get_quantities(new_buy_for_prices, self.order_size_per_side)
            # add more orders
        elif len(self.buy_for) > self.n_orders:
          extra_buy_for_orders = len(self.buy_for) - self.n_orders
          while extra_buy_for_orders != 0:
            new_cancel_orders.append(CancelOrder(market_id=self.market_id, order_hash=self.buy_for.pop().order_hash))
            extra_buy_for_orders -= 1
        else:
          print("Failed to send orders")
          return
      if (len(self.buy_against) != self.n_orders):
        if len(self.buy_against) < self.n_orders:
          for i in range(len(self.buy_against), self.n_orders):
            # FIXME: not good
            new_buy_against_prices.append(prices[1][i])
            new_buy_against_quantities = self._get_quantities(new_buy_against_prices, self.order_size_per_side)
            # add more orders
        elif len(self.buy_against) > self.n_orders:
          extra_buy_against_orders = len(self.buy_against) - self.n_orders
          while extra_buy_against_orders != 0:
            new_cancel_orders.append(
              CancelOrder(market_id=self.market_id, order_hash=self.buy_against.pop().order_hash)
            )
            extra_buy_against_orders -= 1
        else:
          print("Failed to send orders")
          return

      missing_orders = self.get_new_order((new_buy_for_prices, new_buy_against_prices),
                                          (new_buy_for_quantities, new_buy_against_quantities))
      if missing_orders:
        asyncio.run(self.create_orders(missing_orders))

      if new_cancel_orders:
        asyncio.run(self.cancel_orders(new_cancel_orders))

    # if we exit while loop, we send a cancel all order request.
    asyncio.run(self.cancel_all_orders())

  def start(self):
    self.initilization()
    self.strategy()


# FIXME
# 1 what should I do with 3 states marekt
# 2 is buy_for price is always lower than buy_against price
# 3 probabilities data format
# 4 the insufficient fund case
# 5 reduce only case
# 6 when to stop the bot
# 7 if there is an error, cancel all my current open orders

if __name__ == "__main__":
  # We assume the probability data is saved in a json file, this file will be updated every n minutes
  naive_market_maker = NaiveMarketMaker(market_id="market_id", n_orders=10, tick_time_seconds=5)
  naive_market_maker.start()
