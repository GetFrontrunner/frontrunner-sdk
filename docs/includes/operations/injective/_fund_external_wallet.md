## Injective: Fund External Subaccount

Send funds to a separate Injective wallet. This sends from main bank balance to main bank balance.

### Parameters

```python
response = await sdk.injective.fund_external_wallet(10, "FRCOIN", "inj1fjlfjy5adns4msjqch3vqjhesmwjnu9ep045wz")
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `amount` | `int` | ✓ | Amount to send |
| `denom` | `str` | ✓ | Denom identifier |
| `destination_injective_address` | `str` | ✓ | Injective account to send to |

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Injective Transaction ID |
