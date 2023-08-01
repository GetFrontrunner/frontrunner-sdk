# Subaccount Management

## Definition
Subaccounts enable traders to execute transactions through multiple accounts under the same wallet. 
Each subaccount has independent balances, margin and positions and can trade independently.
so they can be used to isolate positions or margin or to run multiple strategies independently.
All orders in Injective markets are from a subaccount (often the default subaccount).

Subaccounts are 0-indexed, and the default subaccount, subaccount 0, has a special 
property: trading from the default subaccount draws funds from the main bank balance. 
Detailed information about this feature can be found [here](https://injective.notion.site/The-new-trading-logic-to-be-introduced-in-v1-10-8b422f7bec6c4cac96459d558e917b6d).

## Properties
* Each subaccount can have a maximum of 20 open orders per market
* A single subaccount cannot create orders for both the `long` and `short` sides in a binary options market

## Sample Code
A simple setup to create liquidity on both sides of a Frontrunner market involves using two non-default 
subaccounts, where one subaccount creates `long` orders and another creates `short` orders.

For example, this is how two subaccounts could be funded with testnet tokens and then used to submit orders
on both sides:

```python
from frontrunner_sdk import FrontrunnerSDKAsync

sdk = FrontrunnerSDKAsync()
wallet = await sdk.wallet()
long_subaccount_index = 1
short_subaccount_index = 2
print(f"Running with wallet {wallet.injective_address}. {long_subaccount_index=}, {short_subaccount_index=}")

response = await sdk.injective.fund_subaccount(1000, "FRCOIN", subaccount_index=long_subaccount_index)
print(f"View deposit transaction to long side subaccount: https://testnet.explorer.injective.network/transaction/{response.transaction}")

response = await sdk.injective.fund_subaccount(1000, "FRCOIN", subaccount_index=short_subaccount_index)
print(f"View deposit transaction to short side subaccount: https://testnet.explorer.injective.network/transaction/{response.transaction}")

probability = 0.30
desired_bid_ask_spread = 0.02
desired_total_liquidity = 100
spread_per_side = desired_bid_ask_spread / 2
response = sdk.injective.create_orders([
  Order.buy_long(some_market, 100, probability + spread_per_side, subaccount_id=long_subaccount_id),
  Order.buy_long(some_market, 100, probability + spread_per_side + 0.01, subaccount_id=long_subaccount_id),
  Order.buy_long(some_market, 300, probability + spread_per_side + 0.02, subaccount_id=long_subaccount_id),
  Order.buy_short(some_market, 100, probability - spread_per_side, subaccount_id=short_subaccount_id),
  Order.buy_short(some_market, 200, probability - spread_per_side - 0.01, subaccount_id=short_subaccount_id),
  Order.buy_short(some_market, 300, probability - spread_per_side - 0.02, subaccount_id=short_subaccount_id),
])
```

Once funded, each subaccount can be used to submit orders for their respective side:
```python

```
