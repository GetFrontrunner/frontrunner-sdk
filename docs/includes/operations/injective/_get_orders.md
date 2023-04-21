## Injective: Get Orders

Gets open orders. For the corresponding Injective API, see [Orders History][order-history].

[order-history]: https://api.injective.exchange/#injectivederivativeexchangerpc-ordershistory

### Parameters

```python
# Get all my orders
response = sdk.injective.get_orders(True)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `mine` | `bool` | ✓ | Only return your orders |
| `market_ids` | `[str]` | ◯ `None` | Only return orders with this market ID |
| `subaccount_id` | `str` | ◯ `None` | Only return orders from this subaccount |
| `direction` | `"buy", "sell"` | ◯ `None` | Only return orders with this direction |
| `state` | `"booked"`, `"partial_filled"`, `"filled"`, `"canceled"` | ◯ `None` | Only return orders in this state |
| `is_conditional` | `bool` | ◯ `None` | Only return orders that are/are not conditional |
| `order_types` | `[str]` | ◯ `None` | Only return orders with these order types |
| `execution_types` | `["limit", "market"]` | ◯ `None` | Only return orders with these execution types |
| `start_time` | `datetime` | ◯ `None` | Only return orders starting on or after this time |
| `end_time` | `datetime` | ◯ `None` | Only return orders ending on or before this time |

### Response

```python
print("orders:")
for order in response.orders:
  print(
    "order:",
    order.order_type,
    order.quantity, "@", order.trigger_price,
    order.order_hash,
  )
```

| Name | Type | Description |
| - | - | - |
| `orders` | `[Order]` | Orders |
