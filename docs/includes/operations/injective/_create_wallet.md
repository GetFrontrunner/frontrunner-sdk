## Injective: Create Wallet

Creates a new wallet with a small aidrop of INJ from the faucet.

### Parameters

```python
response = sdk.injective.create_wallet()
```

There are no parameters for this operation.

### Response

```python
print("wallet eth address:", response.wallet.ethereum_address)
print("wallet inj address:", response.wallet.injective_address)

print("wallet mnenomic (keep this safe):")
print("\n\t", response.wallet.mnemonic)
```

| Name | Type | Description |
| - | - | - |
| `wallet` | `Wallet` | The created wallet |
