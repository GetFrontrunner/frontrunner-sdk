## Injective: Cancel Orders

Cancels specific orders.

### Parameters

```python
# Cancel a single specific order
response = sdk.injective.cancel_orders([
  CancelOrder(
    market_id="0x141e3c92ed55107067ceb60ee412b86256cedef67b1227d6367b4cdf30c55a74",
    order_hash="znihpTtkWn/9Npy1Zzku+GNxXfyLE/k05U1KXRUTO1E=",
  ),
])
```

| Name | Type | | Description |
| - | - | - | - |
| `orders` | `[CancelOrder]` | ✓ | List of order cancellation specs |
| `orders[].market_id` | `str` | ✓ | Market ID of order to cancel |
| `orders[].order_hash` | `str` | ✓ | Order hash of order to cancel |

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Transaction ID of the order cancellation |
