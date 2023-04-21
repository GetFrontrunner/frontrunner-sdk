## Injective: Fund Wallet from Faucet

Request a small amount of INJ from the faucet.

<aside class="notice">
You can only request from the Injective Testnet faucet once every 24 hours.
</aside>

### Parameters

```python
response = sdk.injective.fund_wallet_from_faucet()
```

There are no parameters for this operation.

### Response

```python
print("message:", response.message)
```

| Name | Type | Description |
| - | - | - |
| `message` | `str` | Message from the faucet |
