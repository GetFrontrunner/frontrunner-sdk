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
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Transaction ID of the order cancellation |
