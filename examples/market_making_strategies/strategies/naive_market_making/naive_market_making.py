"""
1. Reads list in the format below, 
2. Processing a new sub-list every tickTimeSeconds 
3. Canceling/re-creating corresponding orders as needed to create a spread of spreadSizeDollars with order sizes of orderSizePerSide
"""
from typing import Tuple
from typing import List
from math import floor
from random import random, randint
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk import FrontrunnerSDK, FrontrunnerSDKAsync
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.cancel_order import CancelOrder
from examples.market_making_strategies.core.market_maker import MarketMaker
from sortedcontainers import SortedDict, SortedKeyList, SortedList
import asyncio
from time import sleep


class NaiveMarketMaker(MarketMaker):
    def __init__(self, market_id:str, n_orders:int):
        super().__init__(market_id=market_id, n_orders=n_orders)
        self.buy_for = SortedKeyList(key=lambda order: -int(order.price))
        self.buy_against = SortedKeyList(key=lambda order: int(order.price))
        self.multiplier = 10
        self.sleep_time = 60


    def float_round_down(self, probability:float, decimal:int=2)->float:
        return floor(probability*(10**decimal))/(10**decimal)

    def read_probability(self,  probability:float):
        pass

    def _get_prices(self):
        pass

    def get_prices(self, probabilities:List[float])->Tuple[List[float], List[float]]:
        buy_for_prices = []#SortedList()
        buy_against_prices = []#SortedList()

        for probability in probabilities:
            #  FIXME buy_for_price << buy_against_price?
            if probability>1-probability:
                buy_for_prices.append(self.float_round_down(probability+self.spread_size_dollars/2))
                buy_against_prices.append(self.float_round_down(1-probability-self.spread_size_dollars/2))
            else:
                buy_for_prices.append(self.float_round_down(probability-self.spread_size_dollars/2)) 
                buy_against_prices.append(self.float_round_down(1-probability+self.spread_size_dollars/2))
        buy_for_prices.sort()
        buy_against_prices.sort(reverse=True)
        return (buy_for_prices, buy_against_prices)

    def _get_quantities(self, prices:List[float], multiplier)->List[int]:
        return [int(multiplier* price) for price in prices]        

    def get_quantities(self, prices:Tuple[List[float], List[float]])->Tuple[List[int],List[int]]:
        buy_for_quantity = self._get_quantities(prices[0],self.multiplier)
        buy_against_quantity = self._get_quantities(prices[1], self.multiplier)
        return (buy_for_quantity, buy_against_quantity)

    def get_new_order(self, prices:Tuple[List[float],List[float]], quantities:Tuple[List[int], List[int]])->List[Order]:
        buy_for = self.build_buy_orders(prices= prices[0], quantities=quantities[0], sides=["for" for _ in quantities])
        buy_against = self.build_buy_orders(prices= prices[1], quantities=quantities[1], sides=["against" for _ in quantities])
        return buy_for + buy_against

            
    def initilization(self):
        self.fund_wallet()

    def strategy(self):
        while True:
            sleep(self.sleep_time)
            if (len(self.buy_for)!=0):
                self.buy_for.clear()
            if (len(self.buy_against)!=0):
                self.buy_against.clear()
                
            probabilities = [random() for _ in range(randint(5,15))]
            prices = self.get_prices(probabilities)
            quantities = self.get_quantities(prices)
            new_orders = self.get_new_order(prices, quantities)
            asyncio.run(self.create_orders(new_orders))

            open_orders = asyncio.run(self.get_my_orders())
            for order in open_orders.orders:
                if order.order_side == "buy":
                    self.buy_for.add(order)
                else:
                    self.buy_against.add(order)

            new_buy_for_prices=[]
            new_buy_against_prices=[]
            new_buy_for_quantities=[]
            new_buy_against_quantities=[]

            new_cancel_orders=[]
            if (len(self.buy_for)!=self.n_orders):
                if len(self.buy_for)<self.n_orders:
                    for i in range(len(self.buy_for), self.n_orders):
                        #FIXME not correct
                        new_buy_for_prices.append(prices[0][i])
                        new_buy_for_quantities = self._get_quantities(new_buy_for_prices, self.multiplier)
                        # add more orders
                elif len(self.buy_for)> self.n_orders:
                    extra_buy_for_orders = len(self.buy_for)-self.n_orders
                    while extra_buy_for_orders!=0:
                        new_cancel_orders.append(CancelOrder(market_id=self.market_id,order_hash=self.buy_for.pop().order_hash))
                        extra_buy_for_orders-=1
                else:
                    print("Failed to send orders")
                    return
            if (len(self.buy_against)!=self.n_orders):
                if len(self.buy_against)<self.n_orders:
                    n_missing_orders=self.n_orders-len(self.buy_against)
                    for i in range(len(self.buy_against), self.n_orders):
                        #FIXME not correct
                        new_buy_against_prices.append(prices[1][i])
                        new_buy_against_quantities = self._get_quantities(new_buy_against_prices, self.multiplier)
                        # add more orders                    
                elif len(self.buy_against) > self.n_orders:
                    extra_buy_against_orders = len(self.buy_against)-self.n_orders
                    while extra_buy_against_orders!=0:
                        new_cancel_orders.append(CancelOrder(market_id=self.market_id,order_hash=self.buy_against.pop().order_hash))
                        extra_buy_against_orders-=1
                else:
                    print("Failed to send orders")
                    return

            missing_orders =self.get_new_order((new_buy_for_prices,new_buy_against_prices),(new_buy_for_quantities,new_buy_against_quantities))
            if missing_orders:
                asyncio.run(self.create_orders(missing_orders))

            if new_cancel_orders:
                asyncio.run(self.cancel_orders(new_cancel_orders))

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
if if __name__ == '__main__':
    naive_market_maker = NaiveMarketMaker(market_id="market_id", n_orders=10)
    naive_market_maker.start()
