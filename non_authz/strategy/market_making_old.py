# Copyright 2022 Injective Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import asyncio
import logging

from pyinjective.composer import Composer as ProtoMsgComposer
from pyinjective.async_client import AsyncClient
from pyinjective.transaction import Transaction
from pyinjective.constant import Network, Denom
from pyinjective.wallet import PrivateKey

from chain.utilities_old import CancelOrder, LimitOrder, MarketOrder, CancelAll

import os
import time


if __name__ == "__main__":
    # pk = os.environ["private_key"]
    pk = "8b97260c40b7e6bf87729299e7af741b46eed5547aa317ddd6fa9bac673ef5d2"
    logging.basicConfig(level=logging.INFO)
    # market_id = "0x64ec31d044fb12929d02d74cc68d3c4a818add11b4b510c120c6e70a7310ab0d"
    market_id = "0x67e7c21141a881919ce150327027ce412aee1a239ca0dd29adb136319dee321b"

    # limit order
    limit_price = 0.62
    quantity = 1
    is_buy = False
    print("\nLIMIT ORDER:")
    order_hash = asyncio.get_event_loop().run_until_complete(
        Limit(limit_price, quantity, is_buy, market_id, pk)
    )
    print(order_hash)

    time.sleep(3)
    limit_price = 0.32
    quantity = 1
    is_buy = True
    print("\nLIMIT ORDER:")
    order_hash = asyncio.get_event_loop().run_until_complete(
        Limit(limit_price, quantity, is_buy, market_id, pk)
    )
    print(order_hash)
    time.sleep(5)

    # market order
    # print("\nMARKET ORDER:")
    # market_price = 0.26
    # asyncio.get_event_loop().run_until_complete(
    #    Market(market_price, quantity, is_buy, market_id, pk)
    # )

    # time.sleep(5)
    # print("\nCANCEL ORDER:")
    # asyncio.get_event_loop().run_until_complete(Cancel(market_id, order_hash, pk))

    time.sleep(5)
    print("\nCANCEL ALL ORDER:")
    asyncio.get_event_loop().run_until_complete(CancelAll(market_id, pk))
