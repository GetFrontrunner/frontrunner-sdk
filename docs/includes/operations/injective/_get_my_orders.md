## Injective: Get My Orders

Gets your open orders. For the corresponding Injective API, see [Subaccount Orders List][subaccount-order-list].

[subaccount-order-list]: https://api.injective.exchange/#injectivederivativeexchangerpc-subaccountorderslist

### Parameters

```python
response = sdk.injective.get_my_orders()
```

There are no parameters for this operation.

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
| `orders` | `[Order]` | Orders open on the account |
