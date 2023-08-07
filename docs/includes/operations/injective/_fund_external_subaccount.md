## Injective: Fund External Subaccount

Send funds to a subaccount that is NOT owned by the SDK wallet.

### Parameters

```python
external_subaccount = Subaccount.from_injective_address_and_index("inj1fjlfjy5adns4msjqch3vqjhesmwjnu9ep045wz", 1)
response = await sdk.injective.fund_external_subaccount(10, "FRCOIN", external_subaccount)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `amount` | `int` | ✓ | Amount to send |
| `denom` | `str` | ✓ | Denom identifier |
| `destination_subaccount` | `Subaccount` | ✓ | Subaccount to send to; cannot be subaccount 0 |
| `source_subaccount_index` | `Optional[int]` | ◯ `None` | If provided, send from SDK wallet's subaccount with this index |

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Injective Transaction ID |
