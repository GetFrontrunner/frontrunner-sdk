## Injective: Refresh Wallet

Refreshes the wallet.

Transactions require a monotonically increasing sequence ID. This sequence ID is tracked internally in the wallet. If the sequence ID known in the wallet drifts for any reason, refreshing the wallet will update the wallet with the latest sequence ID.

### Parameters

None.

```python
response = sdk.injective.refresh_wallet()
```

### Response

```python
print("wallet sequence:", response.wallet.sequence)
```

| Name | Type | Description |
| - | - | - |
| `wallet` | `Wallet` | The internal wallet, same instance as `sdk.wallet()` |
