## Injective: Stream Orders

Get new orders as they arrive. For the corresponding Injective API, see [Stream Order History][stream-order-history].

[stream-order-history]: https://api.injective.exchange/#injectivederivativeexchangerpc-streamordershistory

<aside class="notice">
This operation only exists in the <code>async</code> SDK.
</aside>

### Parameters

```python
async def run():
  market_id = "0x90e662193fa29a3a7e6c07be4407c94833e762d9ee82136a2cc712d6b87d7de3"

  response = async_sdk.injective.stream_orders(market_id)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `market_id` | `str` | ✓ | Market ID to watch for orders |
| `mine` | `bool` | ◯ `False` | Only watch for my orders |
| `direction` | `"buy", "sell"` | ◯ `None` | Only watch for orders of this direction |
| `subaccount_id` | `bool` | ◯ `False` | Only watch for my orders from this subaccount |
| `order_types` | `bool` | ◯ `False` | Only watch for orders of this type |
| `state` | `bool` | ◯ `False` | Only watch for orders of this state |
| `execution_types` | `bool` | ◯ `False` | Only watch for orders of this type |

### Response

```python
async def run():
  response = ...

  async for order in response.orders:
    print("order:", order.operation_type, order.order.order_hash)
```

| Name | Type | Description |
| - | - | - |
| `orders` | `AsyncIterator[DerivativeOrderHistory]` | Iterator for orders |