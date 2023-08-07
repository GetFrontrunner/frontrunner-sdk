## Injective: Withdraw from Subaccount

Withdraw funds from a subaccount that IS owned by the SDK wallet to the main bank balance.

### Parameters

```python
response = await sdk.injective.withdraw_from_subaccount(10, "FRCOIN", subaccount_index=1)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `amount` | `int` | ✓ | Amount to send |
| `denom` | `str` | ✓ | Denom identifier |
| `subaccount_index` | `int` | ✓ | Withdraw from SDK wallet's subaccount with this index |

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Injective Transaction ID |
