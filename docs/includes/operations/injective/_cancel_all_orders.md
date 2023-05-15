## Injective: Cancel All Orders

Cancel all your open orders.

### Parameters

```python
# Cancel all your orders
response = sdk.injective.cancel_all_orders()
```

There are no parameters for this operation.

### Response

```python
print("transaction:", response.transaction)
print("orders:")
for order in response.orders:
  print(f"\tmarket: {order.market_id[:12]}... price: {order.price} quantity: {order.quantity}")
```

| Name | Type | Description |
| - | - | - |
| `orders` | `Iterable[DerivativeLimitOrder]` | Cancelled orders |
| `transaction` | `Optional[str]` | Transaction ID of the order cancellation |
