# Quickstart

To demonstrate SDK usage, we'll be using it to create a wallet, place a market order, and listing our orders.

## Installation

```sh
pip install -y frontrunner-sdk
```

## Creating and Funding a Wallet

```python
from frontrunner_sdk import FrontrunnerSDK

# Create a synchronous Frontrunner SDK
# By default, this will use testnet; no "real" tokens will be involved.
sdk = FrontrunnerSDK()

# Creates a new wallet locally
# Requests funds from an 
create_wallet = sdk.injective.create_wallet()

# Save your wallet credentials
print(f"""
Put this somewhere safe!

    {create_wallet.wallet.mnemonic}

""")
```

## Getting Frontrunner Markets

```python
find_markets = sdk.frontrunner.find_markets(
  sports=["basketball"], # Looking for basketball game markets
  event_types=["game"], # Looking for game (instead of future) markets
  prop_types=["winner"], # Looking for winner (instead of loser/other) markets
)

# Pick a market
market = find_markets.markets[0]
print(f"Market: {market.long_entity_name} [{market.prop_name}] vs {market.short_entity_name}")
```

## Finding Current Low & High Bids

```python
# get the order book for this market
get_order_books = sdk.injective.get_order_books([market.injective_id])
orders = get_order_books.order_books[market.injective_id]

# print order book buys
print("buys:")
for buy in orders.buys:
  print(f"{buy.quantity} @ {buy.price}")

# print order book sells
print("sells:")
for sell in orders.sells:
  print(f"{sell.quantity} @ {sell.price}")

# find the lowest and highest buying prices in the order book
prices = [int(buy.price) / 1000000 for buy in orders.buys]
highest_buy, lowest_buy = max(prices), min(prices)
print(f"price range: [{highest_buy}, {lowest_buy}]")
```

## Placing bids

```python
from frontrunner_sdk.models import Order

create_orders = sdk.injective.create_orders([
  Order.buy_for(market.injective_id, 10, lowest_buy),
  Order.buy_for(market.injective_id, 100, (highest_buy + lowest_buy) / 2),
  Order.buy_for(market.injective_id, 10, highest_buy),
])

print(f"""
Transaction: {create_orders.transaction}

You can view your transaction at:

  https://testnet.explorer.injective.network/transaction/{create_orders.transaction}

""")
```

## Retrieving Your Orders

```python
get_my_orders = sdk.injective.get_my_orders()

print("my orders:")
for order in get_my_orders.orders:
  print(f"{order.order_hash}: {order.quantity} @ {order.price}")
```
