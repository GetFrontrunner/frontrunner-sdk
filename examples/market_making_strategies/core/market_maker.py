import asyncio
from typing import Tuple
from typing import List
from typing import Literal
from frontrunner_sdk.sdk import FrontrunnerSDKAsync
from frontrunner_sdk.models.order import Order
from frontrunner_sdk.models.cancel_order import CancelOrder

"""
1. fund wallet
2. get market id
3. check prob
4. send orders
5. listen for the trade steam
6. refresh current orders
"""

class MarketMaker:
    def __init__(self, market_id:str, n_orders:int=10) -> None:
        self.async_sdk = FrontrunnerSDKAsync()
        self.async_fr = self.async_sdk.frontrunner
        self.async_inj = self.async_sdk.injective
        self.wallet = self._get_wallet()
        self.market_id = market_id
        self.n_orders = n_orders

    def _get_wallet(self):
        return asyncio.run(self.async_sdk.wallet())
 
    def fund_wallet(self):
        return asyncio.run(self.async_inj.fund_wallet_from_faucet()) 
    def find_market(self):
        # TODO what to do with this
        return asyncio.run(self.async_fr.find_markets())

    def get_probabilities(self, probability:float)->List[List[float]]:
        # TODO what to feed in this function
        return [[0.1], [0.9]]

    def get_quantities(self, probabilities:List[float])->List[float]:
        return [10* probability for probability in probabilities]

    def build_buy_orders(self, prices:List[float], quantities:List[int], sides:List[Literal["for", "against"]])-> List[Order]:
        zipped_orders = zip(prices,quantities,sides)
        return [Order(direction='buy', side=order[2], market_id=self.market_id, quantity=order[1], price=order[0]) for order in zipped_orders]

    def build_sell_orders(self, prices:List[float], quantities:List[int], sides:List[Literal["for", "against"]])->List[Order]:
        # check current position
        # maybe better to skip the check the current position
        # if no enough position this will fail 
        zipped_orders = zip(prices,quantities,sides)
        return [Order(direction='sell', side=order[2], market_id=self.market_id, quantity=order[1], price=order[0]) for order in zipped_orders]

    async def create_orders(self, orders:List[Order]):
        return await self.async_inj.create_orders(orders)

    async def cancel_orders(self, orders:List[CancelOrder]):
        return await self.async_inj.cancel_orders(orders)

    async def trades_stream(self):
        return await self.async_inj.stream_trades(self.market_id, mine=True)

    async def order_book(self):
        return await self.async_inj.get_order_books(self.market_id)

    async def get_my_orders(self):
        return await self.async_inj.get_my_orders()

    async def get_my_positions(self):
        return await self.async_inj.get_positions(self.market_id, mine=True)

    async def get_account_portfolio(self):
        return await self.async_inj.get_account_portfolio()

    async def cancel_all_orders(self):
        return await self.async_inj.cancel_all_orders()

    def strategy(self):
        raise NotImplemented

    def initilization(self):
        raise NotImplemented

    def start(self):
        raise NotImplemented


