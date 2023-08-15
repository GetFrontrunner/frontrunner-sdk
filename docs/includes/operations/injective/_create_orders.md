## Injective: Create Orders

Create orders. Order has a market, price, and quantity.

For finding markets, see `find_markets`.

### Parameters

```python
some_market = "0x141e3c92ed55107067ceb60ee412b86256cedef67b1227d6367b4cdf30c55a74"
other_market = "0x9181874b70fefe3e126b6472c6de647b4dbfa59025ad5dc61be6559532d19e15"

# Create orders 
# Note that this specific set of orders (both long and short buys) can't all be executed together due to subaccount
#   mechanics (see Subaccount Management for more details) and because sells only work with an existing position. 
#   This list of orders is just to demonstrate all types.
response = sdk.injective.create_orders([
  Order.buy_long(some_market, 120, 0.70),
  Order.sell_long(some_market, 100, 0.75),
  Order.buy_short(other_market, 30, 0.90),
  Order.sell_short(other_market, 25, 0.95),
])
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `orders` | `[Order]` | ✓ | Orders to place; must have at least 1 order |
| `orders[].market_id` | `str` | ✓ | Market of the order |
| `orders[].quantity` | `int` | ✓ | How many orders to place |
| `orders[].price` | `float` | ✓ | At what price to place the order; must be 0 < price < 1 |
| `orders[].subaccount_index` | `int` | ◯ `0` | Index of the subaccount to create the order from |
| `orders[].is_post_only` | `bool` | ◯ `False` | If True, this is a post-only order that will only succeed if it enters the orderbook unmatched |

<aside class="warning">
If a post-only order would match with an existing order, the operation will still return a transaction hash 
but transaction logs will show failure with <a href="https://api.injective.exchange/#error-codes">error code</a> <code>59</code>.
The error code can be seen with the SDK's `get_transaction` operation or 
<a href="https://api.injective.exchange/#account-streameventorderfail">StreamEventOrderFail</a>.
See <a href="https://testnet.explorer.injective.network/transaction/BAE72A64BE091B323F508F1887FAF4FA94C0EFE9348831C07DBB078CFC71E16A/event-logs/">an example failed transaction's Event Logs in the testnet Explorer</a>
</aside>

### Response

```python
print("transaction:", response.transaction)

for order in response.orders:
  print(
    "order:",
    order.market_id,
    "for", order.quantity, "@" order.price,
    "in subaccount", order.subaccount_index,
    "with hash", order.hash,
  )
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Transaction ID of the order creation |
| `orders` | `List[Order]` | Orders from input, but with `hash` defined |
