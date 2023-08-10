# Subaccount Management

## Definition
Subaccounts enable traders to execute transactions through multiple accounts under the same wallet. 
Each subaccount has independent balances, margin and positions and can trade independently.
so they can be used to isolate positions or margin or to run multiple strategies independently.
All orders in Injective markets are from a subaccount (often the default subaccount).

Subaccounts are 0-indexed, and the default subaccount, subaccount 0, has a special 
property: trading from the default subaccount draws funds from the **main bank balance**.
Detailed information about this feature can be found [here](https://injective.notion.site/The-new-trading-logic-to-be-introduced-in-v1-10-8b422f7bec6c4cac96459d558e917b6d).
The main bank balance is associated with the Injective address (e.g. `inj14w0zfp47jqpgjst87vxg5ydgvtevfdm38338xp`).
Subaccount balances are associated with each subaccount (e.g. `0xb4efdbe3240d3d2a1bc6be8a1f717944e734a0dd000000000000000000000000`).

## Properties
* Each subaccount can have a maximum of 20 open orders per market
* A single subaccount cannot create orders for both the `long` and `short` sides in a binary options market

## Transferring Funds
These are the operations involved in transferring funds between accounts or subaccounts:

| Operation                  | Usage                                                                                                                                                           | Notes                                                                                                    |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| `fund_external_subaccount` | Send funds to a subaccount that is NOT owned by the SDK wallet.                                                                                                 | Cannot fund subaccount 0.                                                                                |
| `fund_external_wallet`     | Send funds to a another Injective wallet.                                                                                                                       | This sends from the configured SDK wallet's main bank balance to the external wallet's main bank balance |
| `fund_subaccount`          | Send funds from the main bank balance to a subaccount that IS owned by the SDK wallet. Or send funds between subaccounts that ARE BOTH owned by the SDK wallet. | Cannot fund subaccount 0. Funding from source subaccount 0 sends from the main bank balance.             |
| `withdraw_from_subaccount` | Withdraw funds from a subaccount that IS owned by the SDK wallet to the main bank balance.                                                                      | Cannot withdraw from subaccount 0.                                                                       |

Where operations involve subaccounts owned by the SDK wallet, either a `Subaccount` object or an integer `index` can be provided for convenience.  
A `Subaccount` object can be created in a few different ways:

```python
from frontrunner_sdk.models import Subaccount, Wallet

wallet = Wallet._new()

Subaccount.from_subaccount_id("0xb4efdbe3240d3d2a1bc6be8a1f717944e734a0dd000000000000000000000001")
wallet.subaccount(1)
Subaccount.from_injective_address_and_index("inj1knhahceyp57j5x7xh69p7utegnnnfgxavmahjr", 1)
Subaccount.from_ethereum_address_and_index("0xb4efdbe3240d3d2a1bc6be8a1f717944e734a0dd", 1)
```


## Sample Code: Market Making
A simple setup to create liquidity on both sides of a Frontrunner market involves using two non-default 
subaccounts, where one subaccount creates `long` orders and another creates `short` orders.

For example, this is how two subaccounts could be funded with testnet tokens and then used to submit orders
on both sides:

```python
import time
from typing import List

from frontrunner_sdk import FrontrunnerSDKAsync
from frontrunner_sdk.models import Order, OrderType

FRCOIN_SCALE_FACTOR = 10 ** 6


async def _print_orderbook(sdk: FrontrunnerSDKAsync, injective_market_id: str):
  response = await sdk.injective.get_order_books([injective_market_id])
  order_book = response.order_books[injective_market_id]

  print("buys:")
  for buy in order_book.buys:
    print(f"  {buy.quantity} @ ${int(buy.price) / FRCOIN_SCALE_FACTOR}")
  print("sells:")
  for sell in order_book.sells:
    print(f"  {sell.quantity} @ ${int(sell.price) / FRCOIN_SCALE_FACTOR}")

  buy_prices = [int(order.price) / FRCOIN_SCALE_FACTOR for order in order_book.buys]
  sell_prices = [int(order.price) / FRCOIN_SCALE_FACTOR for order in order_book.sells]
  highest_buy, lowest_sell = max(buy_prices) if buy_prices else 0, min(sell_prices) if sell_prices else 0
  print(f"bid-ask spread: [${highest_buy}, ${lowest_sell}]")

async def _print_orders(sdk: FrontrunnerSDKAsync, injective_market_id: str, subaccount_indexes: List[int]):
  for subaccount_index in subaccount_indexes:
    get_orders = await sdk.injective.get_orders(mine=True, market_ids=[injective_market_id], subaccount_index=subaccount_index)
    print(f"orders for index {subaccount_index}:")
    for order_history in get_orders.orders:
      print(f"{order_history.order_type} {order_history.order.state} : filled {order_history.order.filled_quantity} / {order_history.order.quantity} @ ${int(float(order_history.order.price)) / FRCOIN_SCALE_FACTOR}")

def calculate_price(probability: float, price_margin: float, order_type: OrderType):
  if order_type == OrderType.BUY_LONG:
    return round(max(0.01, min(0.99, probability - price_margin)), 2)
  else:
    return round(min(0.99, max(0.01, probability + price_margin)), 2)

def generate_histogram_orders(injective_market_id: str, total_value_coefficients: List[float], order_type: OrderType, price: float, price_step: float, total_value: float, subaccount_index: int):
  orders = []
  for coeff in total_value_coefficients:
    if price < 0.01 or price > 0.99:
      break
    coeff_total_value = total_value * coeff # total amount we want to spend on shares at this price
    num_shares = coeff_total_value / price # num_shares * price = total_value spent
    if order_type == OrderType.BUY_LONG:
      orders.append(Order.buy_long(injective_market_id, int(round(num_shares, 0)), round(price, 2), subaccount_index=subaccount_index))
    elif order_type == OrderType.BUY_SHORT:
      orders.append(Order.buy_short(injective_market_id, int(round(num_shares, 0)), round(price, 2), subaccount_index=subaccount_index))
    price += price_step
  return orders

async def main():
  total_value_coefficients = [0.2, 0.3, 0.5] # the distribution of funds for each price step; sum should always equal 1
  assert(int(sum(total_value_coefficients)) == 1)
  sdk = FrontrunnerSDKAsync()
  print(f"Running with wallet {(await sdk.wallet()).injective_address}")
  injective_market_id = "REPLACE_ME"

  wallet = await sdk.wallet()
  long_subaccount_index = 1
  short_subaccount_index = 2
  long_subaccount = wallet.subaccount_address(long_subaccount_index)
  short_subaccount = wallet.subaccount_address(short_subaccount_index)
  print(f"Running with wallet {wallet.injective_address}. {long_subaccount=}, {short_subaccount=}")

  response = await sdk.injective.fund_subaccount(1000, "FRCOIN", destination_subaccount_index=long_subaccount_index)
  print(f"View deposit transaction to long side subaccount: https://testnet.explorer.injective.network/transaction/{response.transaction}")

  response = await sdk.injective.fund_subaccount(1000, "FRCOIN", destination_subaccount_index=short_subaccount_index)
  print(f"View deposit transaction to short side subaccount: https://testnet.explorer.injective.network/transaction/{response.transaction}")

  probability = 0.68
  desired_total_liquidity = 100
  spread_per_side = 0.01
  long_base_price = calculate_price(probability, spread_per_side, OrderType.BUY_LONG)
  short_base_price = calculate_price(probability, spread_per_side, OrderType.BUY_SHORT)
  # Note this includes validation of the probability to prevent submitting orders at invalid prices.
  #   Instead, this case could be detected and a smaller histogram created.
  buy_long_orders = generate_histogram_orders(injective_market_id, total_value_coefficients, OrderType.BUY_LONG, long_base_price, -1 * spread_per_side, desired_total_liquidity / 2, long_subaccount_index) if probability >= 0.02 else []
  buy_short_orders = generate_histogram_orders(injective_market_id, total_value_coefficients, OrderType.BUY_SHORT, short_base_price, spread_per_side, desired_total_liquidity / 2, short_subaccount_index)  if probability <= 0.98 else []
  orders = buy_long_orders + buy_short_orders
  print(orders)
  response = await sdk.injective.create_orders(orders)
  print(f"View create orders transaction: https://testnet.explorer.injective.network/transaction/{response.transaction}")
  time.sleep(5)  # ensure new state is reflected
  await _print_orderbook(sdk, injective_market_id)
  await _print_orders(sdk, injective_market_id, list(range(3)))
```
