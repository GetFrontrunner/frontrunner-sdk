# Quickstart

To demonstrate SDK usage, we'll be using it to create a wallet, place a market order, and listing our orders.

## Installation

First install the [Injective SDK pre-requisites][injective-sdk-prereqs].

[injective-sdk-prereqs]: https://github.com/InjectiveLabs/sdk-python#dependencies

```sh
pip install frontrunner-sdk
```

Then install the Frontrunner SDK.

Contact [support@getfrontrunner.com][support] for a Frontrunner API Key. Keep this somewhere safe. When launching a Python REPL or running the scripts in this guide, make sure that API Key is set in the environment variable `FR_PARTNER_API_TOKEN`.

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

> **Output**

```text
Put this somewhere safe!

    bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39 bip39
```

In a script or Python REPL, run the following code.

This will create an instance of the SDK which will be used to interact with both Frontrunner and Injective. There are two "versions" of this SDK: synchronous and asynchronous. For this quickstart, we will use the synchronous version.

Then, we'll call `create_wallet` to create our wallet and receive an airdrop from Injective's faucet, to allow us to start placing orders right away! Any subsequent calls that require a wallet will use the one we just made.

## Getting Frontrunner Markets

```python
find_markets = sdk.frontrunner.find_markets(
  sports=["basketball"], # Looking for basketball game markets
  event_types=["game"], # Looking for game (instead of future) markets
  prop_types=["winner"], # Looking for winner (instead of other) markets
  market_statuses=["active"], # Only active markets
)

# Pick a market
market = find_markets.markets[0]
print(f"Market: {market.long_entity_name} [{market.prop_name}] vs {market.short_entity_name}")
```

> **Output**

```text
Market: New York Knicks [Winner] vs Cleveland Cavaliers
```

Before we can bet on markets, we'll need to find them. The example here finds all markets where the sport is basketball, the event is a game, and the proposition is for a winner. The response object contains the raw market objects and the market IDs, which will be useful for placing bets.

Then, we'll pick one market to place bets on, and print some info about it.

## View an Order Book

```python
# get the order book for this market
response = sdk.injective.get_order_books([market.injective_id])
order_book = response.order_books[market.injective_id]

# Frontrunner testnet markets are in FRCOIN and on Injective, FRCOIN has 6 decimals.
# 1,000,000 from Injective is $1 FRCOIN.
FRCOIN_SCALE_FACTOR = 10 ** 6

# print order book buys
print("buys:")
for buy in order_book.buys:
  print(f"  {buy.quantity} @ ${int(buy.price) / FRCOIN_SCALE_FACTOR}")

# print order book sells
print("sells:")
for sell in order_book.sells:
  print(f"  {sell.quantity} @ ${int(sell.price) / FRCOIN_SCALE_FACTOR}")

# find the highest buy and lowest sell
buy_prices = [int(order.price) / FRCOIN_SCALE_FACTOR for order in order_book.buys]
sell_prices = [int(order.price) / FRCOIN_SCALE_FACTOR for order in order_book.sells]
highest_buy, lowest_sell = max(buy_prices), min(sell_prices)
print(f"bid-ask spread: [${highest_buy}, ${lowest_sell}]")
```

> **Output**

```text
buys:
  5882 @ $0.34
  9091 @ $0.33
  15625 @ $0.32
  5000 @ $0.1
sells:
  4364 @ $0.36
  8108 @ $0.37
  13158 @ $0.38
bid-ask spread: [$0.34, $0.36]
```

Without knowing much else about the market besides its ID, it's hard to price bets and make orders. Here, we'll place multiple buy orders above the highest buy price.

We'll call `get_order_books`, passing in the Injective market id, to get the current order book. This order book contains both the buys and sells. Using the buys, we can find the highest buy price.

## Placing buy orders

```python
from frontrunner_sdk.models import Order

highest_buy = 0.01
injective_id = "0xd03091c74e4e76878c2afbeb470b1c825677014afdaa3d315fa534884d2d90e1"

create_orders = sdk.injective.create_orders([
    Order.buy_long(injective_id, 10, highest_buy + 0.01),
    Order.buy_long(injective_id, 5, highest_buy + 0.02),
])

print(f"""
Transaction: {create_orders.transaction}

You can view your transaction at:

  https://testnet.explorer.injective.network/transaction/{create_orders.transaction}
""")
```

> **Output**

```text
Transaction: 917F980F001120A05642F225E9197CCDF1BB5677A6381F81D2CC95410466008C

You can view your transaction at:

  https://testnet.explorer.injective.network/transaction/917F980F001120A05642F225E9197CCDF1BB5677A6381F81D2CC95410466008C
```

To place the orders, we'll call `create_orders`. We'll place...

* An order for 10 shares at $0.01 above the highest buy price
* An order for 5 shares at $0.02 above the highest buy price

Note that we use a hard-coded market ID here that points to a testnet USDT market that can be traded in with Injective Faucet funds.

Contact [support@getfrontrunner.com][support] to request testnet FRCOIN to trade in real Frontrunner markets.

## Retrieving Your Orders

```python
get_orders = sdk.injective.get_orders(mine=True, execution_types=["limit"])

print("orders:")
for order_history in get_orders.orders:
  print(f"  {order_history.order_type} {order_history.order.order_hash}: {order_history.order.quantity} @ ${int(order_history.order.price) / FRCOIN_SCALE_FACTOR}")
```

> **Output**

```text
orders:
  OrderType.BUY_LONG 0x642c138d85a8224093665d1c8bd4fc31e2307fcee62157c7175e5865ea850247: 5 @ $0.03
  OrderType.BUY_LONG 0xd82ced802fdf5ce55a1b37238d83ece7677e4aeb0d576ebb76d041a590ecff16: 10 @ $0.02
```
