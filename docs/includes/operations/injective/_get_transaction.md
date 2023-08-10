## Injective: Get Transaction

Gets open positions. For the corresponding Injective API, see [GetTx][get-tx].

[get-tx]: https://api.injective.exchange/#account-gettx

### Parameters

```python
transaction_hash = "BAE72A64BE091B323F508F1887FAF4FA94C0EFE9348831C07DBB078CFC71E16A"

# Get all buy positions
response = sdk.injective.get_transaction(transaction_hash)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `transaction_hash` | `str` | ✓ | Injective transaction hash |

### Response

```python
print("raw injective response:", response.injective_response)
print("order failures:", response.order_failures)
```

| Name | Type | Description |
| - | - | - |
| `injective_response` | `GetTxResponse` | Raw Injective response |
| `order_failures` | `List[OrderFailure]` | If order failures are found in the logs, list of those failures |
| `order_failures[].flags` | `List[int]` | Flags (error codes) of the order failure. See https://api.injective.exchange/#error-codes |
| `order_failures[].hashes` | `List[str]` | Hashes of the order failure |
