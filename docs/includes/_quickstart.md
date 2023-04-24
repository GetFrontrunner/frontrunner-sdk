# Quickstart

To demonstrate SDK usage, we'll be using it to create a wallet, place a market order, and listing our orders.

## Installation

```sh
pip install -y frontrunner-sdk
```

Install the Frontrunner SDK using the following code.

Contact [support@getfrontrunner.com][support] for a Frontrunner API Key. Keep this somewhere safe. When launching a Python REPL or running the scripts in this guide, make sure that API Key is set in the environment variable `FRONTRUNNER_PARTNER_API_AUTHN_TOKEN`.

[support]: mailto:support@getfrontrunner.com

## Creating and Funding a Wallet

```python
from frontrunner_sdk import FrontrunnerSDK

# Create a synchronous Frontrunner SDK
# By default, this will use testnet; no "real" tokens will be involved.
sdk = FrontrunnerSDK()

# Creates a new wallet locally
# Requests funds from an injective faucet
create_wallet = sdk.injective.create_wallet()

# Save your wallet credentials
print(f"""
Put this somewhere safe!

    {create_wallet.wallet.mnemonic}

""")
```

In a script or Python REPL, run the following code.

This will create an instance of the SDK which will be used to interact with both Frontrunner and Injective. There are two "versions" of this SDK: synchronous and asynchronous. For this quickstart, we will use the synchronous version.

Then, we'll call `create_wallet` to create our wallet and receive an airdrop from Injective's faucet, to allow us to start placing orders right away! Any subsequent calls that require a wallet will use the one we just made.

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

Before we can bet on markets, we'll need to find them. The example here finds all markets where the sport is basketball, the event is a game, and the proposition is for a winner. The response object contains (among other things) the raw market objects and the market IDs, which will be useful for placing bets.

Then, we'll pick one market to place bets on, and print some info about it.

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

# Frontrunner markets are in USDC while on Injective, USDC has 6 decimals.
# 1,000,000 from Injective is $1 USDC.
INJ_TO_USDC = 10 ** -6

# find the lowest and highest buying prices in the order book
prices = [int(buy.price) * INJ_TO_USDC for buy in orders.buys]
highest_buy, lowest_buy = max(prices), min(prices)
print(f"price range: [{highest_buy}, {lowest_buy}]")
```

Without knowing much else about the market besides its ID, it's hard to price bets and make orders. Here, we'll use our top-secret proprietary trading algorithm: we'll place buy bids around the current min, max, and midway buy prices.

We'll call `get_order_books`, passing in our market id, to get the current order books. This order book contains both the buys and sells. Using the buys, we can find the highest and lowest buy prices.

## Placing bids

```python
from frontrunner_sdk.models import Order

create_orders = sdk.injective.create_orders([
    Order.buy_long(market.injective_id, 10, lowest_buy),
    Order.buy_long(market.injective_id, 100, (highest_buy + lowest_buy) / 2),
    Order.buy_long(market.injective_id, 10, highest_buy),
])

print(f"""
Transaction: {create_orders.transaction}

You can view your transaction at:

  https://testnet.explorer.injective.network/transaction/{create_orders.transaction}

""")
```

To place the orders, we'll call `create_orders`. We'll place...

* 10 orders of the lowest price
* 100 orders of the midway price
* 10 orders of the highest price

## Retrieving Your Orders

```python
get_orders = sdk.injective.get_orders(mine=True)

print("orders:")
for order in get_orders.orders:
  print(f"{order.order_hash}: {order.quantity} @ {order.price}")
```
