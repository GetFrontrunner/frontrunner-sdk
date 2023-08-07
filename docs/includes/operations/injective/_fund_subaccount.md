## Injective: Fund Subaccount

Send funds from the main bank balance to a subaccount that IS owned by the SDK wallet. Or send funds between subaccounts that ARE BOTH owned by the SDK wallet.

### Parameters

```python
destination_subaccount_index = 2
wallet = await sdk.wallet()
destination_subaccount = Subaccount.from_wallet_and_index(wallet, destination_subaccount_index)

# Equivalent methods of transferring from main bank balance to a subaccount
response = await sdk.injective.fund_subaccount(5, "FRCOIN", destination_subaccount_index=1)
response = await sdk.injective.fund_subaccount(5, "FRCOIN", destination_subaccount=destination_subaccount)

# Equivalent methods of transferring between subaccounts
response = await sdk.injective.fund_subaccount(5, "FRCOIN", source_subaccount_index=1, destination_subaccount_index=destination_subaccount_index)
response = await sdk.injective.fund_subaccount(5, "FRCOIN", source_subaccount_index=1, destination_subaccount=destination_subaccount)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `amount` | `int` | ✓ | Amount to send |
| `denom` | `str` | ✓ | Denom identifier |
| `destination_subaccount` | `Optional[Subaccount]` | ◯ `None` | Subaccount to send to; cannot be subaccount 0. |
| `destination_subaccount_index` | `Optional[int]` | ◯ `None` | Subaccount to send to; cannot be subaccount 0 |
| `source_subaccount_index` | `Optional[int]` | ◯ `None` | If provided, send from SDK wallet's subaccount with this index |

`destination_subaccount` and `destination_subaccount_index` are mutually exclusive, and at least one must be specified.

### Response

```python
print("transaction:", response.transaction)
```

| Name | Type | Description |
| - | - | - |
| `transaction` | `str` | Injective Transaction ID |
