## Injective: Get Orders

Gets open orders. For the corresponding Injective API, see [Orders History][order-history].

[order-history]: https://api.injective.exchange/#injectivederivativeexchangerpc-ordershistory

### Parameters

```python
# Get all my orders
response = sdk.injective.get_orders(mine=True)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `mine` | `bool` | ◯ `None` | Only return your orders |
| `market_ids` | `[str]` | ◯ `None` | Only return orders with this market ID |
| `subaccount_id` | `str` | ◯ `None` | Only return orders from this subaccount* |
| `subaccount` | `Subaccount` | ◯ `None` | Only return orders from this subaccount. May replace `subaccount_id` in the future |
| `subaccount_index` | `int` | ◯ `None` | Only return orders from this subaccount index. Requires `mine=True` if provided |
| `direction` | `"buy", "sell"` | ◯ `None` | Only return orders with this direction |
| `state` | `"booked"`, `"partial_filled"`, `"filled"`, `"canceled"` | ◯ `None` | Only return orders in this state |
| `is_conditional` | `bool` | ◯ `None` | Only return orders that are/are not conditional |
| `order_types` | `[str]` | ◯ `None` | Only return orders with these order types |
| `execution_types` | `["limit", "market"]` | ◯ `None` | Only return orders with these execution types |
| `start_time` | `datetime` | ◯ `None` | Only return orders starting on or after this time |
| `end_time` | `datetime` | ◯ `None` | Only return orders ending on or before this time |

*Only one of `subaccount_id`, `subaccount`, or `subaccount_index` may be provided.


### Response

```python
print("orders:")
for order_history in response.orders:
  print(
    "order:",
    order_history.order_type,
    order_history.order.quantity, "@", order_history.order.trigger_price,
    order_history.order.order_hash,
  )
```

| Name | Type | Description |
| - | - | - |
| `orders` | `[OrderHistory]` | Orders |
