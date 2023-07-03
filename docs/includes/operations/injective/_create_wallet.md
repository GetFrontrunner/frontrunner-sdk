## Injective: Create Wallet

Creates a new wallet with a small aidrop of INJ and USDT from Injective's faucet.

### Parameters

```python
response = sdk.injective.create_wallet()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `fund_and_initialize` | `bool` | ◯ `True` | If true, fund the wallet from the testnet faucet and initialize (only functions on `testnet`) |

### Response

```python
print("wallet eth address:", response.wallet.ethereum_address)
print("wallet inj address:", response.wallet.injective_address)

print("wallet mnenomic (keep this safe):")
print("\n\t", response.wallet.mnemonic)
print("wallet private key (keep this safe):")
print("\n\t", response.wallet.private_key.to_hex())
```

| Name | Type | Description |
| - | - | - |
| `wallet` | `Wallet` | The created wallet |
