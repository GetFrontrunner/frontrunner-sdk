## Injective: Create Orders

Create orders. Order has a market, price, and quantity.

For finding markets, see `find_markets`.

### Parameters

```python
some_market = "0x141e3c92ed55107067ceb60ee412b86256cedef67b1227d6367b4cdf30c55a74"
other_market = "0x9181874b70fefe3e126b6472c6de647b4dbfa59025ad5dc61be6559532d19e15"

# Create buy orders
response = sdk.injective.create_orders([
  Order.buy_for(some_market, 120, 0.70),
  Order.buy_for(other_market, 30, 0.90),
])
```

| Name | Type | | Description |
| - | - | - | - |
| `orders` | `[Order]` | ✓ | Orders to place; must have at least 1 order |
| `orders[].market_id` | `str` | ✓ | Market of the order |
| `orders[].quantity` | `int` | ✓ | How many orders to place |
| `orders[].price` | `float` | ✓ | At what price to place the order; must be 0 < price < 1 |

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Transaction ID of the order creation |
