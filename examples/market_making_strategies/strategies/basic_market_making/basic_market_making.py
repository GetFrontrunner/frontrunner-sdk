"""
1. Reads list in the format below, 
2. Processing a new sub-list every tickTimeSeconds 
3. Canceling/re-creating corresponding orders as needed to create a spread of spreadSizeDollars with order sizes of orderSizePerSide
"""
from typing import Tuple
from typing import List
from math import floor
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk import FrontrunnerSDK, FrontrunnerSDKAsync
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.order_data import OrderData


class MarketMaking:
    def __init__(self, market_id:str, tick_time_seconds:int, spread_size_dollars:float, order_size_per_side:int):
        self.market_id = market_id
        self.tick_time_seconds = tick_time_seconds
        self.spread_size_dollars = spread_size_dollars
        self.order_size_per_side = order_size_per_side
        self.async_sdk_fr = FrontrunnerSDKAsync()
        self.async_fr = self.async_sdk_fr.frontrunner
        self.async_inj = self.async_sdk_fr.injective

    def float_round_down(self, probability:float, decimal:int=2)->float:
        return floor(probability*(10**decimal))/(10**decimal)

    def read_probability(self,  probability:float):
        pass

    def get_prices(self, probability:float)->Tuple[float, float]:
        if probability>1-probability:
            return (
                self.float_round_down(probability+self.spread_size_dollars/2), 
                self.float_round_down(1-probability-self.spread_size_dollars/2)
            ) 
        else:
            return (
                self.float_round_down(probability-self.spread_size_dollars/2), 
                self.float_round_down(1-probability+self.spread_size_dollars/2)
            )
            

    def get_quanities(self, prices:Tuple[float, float])->Tuple[int, int]:
        return (self.order_size_per_side, self.order_size_per_side)

    def get_order(self, prices:Tuple[float,float], quantities:Tuple[int, int])->Tuple[Order, Order]:
        buy_for = Order.buy_for(self.market_id, quantities[0], prices[0])
        buy_against = Order.sell_for(self.market_id, quantities[1], prices[1])
        return (buy_for, buy_against)

    async def create_orders(self, orders:List[Order]):
        return await self.async_sdk_fr.injective.create_orders(orders)

    async def get_order_books(self):
        return await self.async_sdk_fr.injective.get_order_books(list(self.market_id))

    async def get_my_orders(self):
        return await self.async_sdk_fr.injective.get_my_orders()

    async def cancel_orders(self, orders:List[Order]):
        return await self.async_sdk_fr.injective.cancel_orders(orders)

    def send_orders(self):
        pass

    def trades_stream(self):
        pass

