## Injective: Get Account Portfolio

Retrieves the account portfolio for the current wallet. For the corresponding Injective API, see [Account Portfolio][get-account-portfolio].

[get-account-portfolio]: https://api.injective.exchange/#injectiveportfoliorpc-accountportfolio

### Parameters

```python
response = sdk.injective.get_account_portfolio()
```

There are no parameters for this operation.

### Response

```python
print("portfolio bank balances:")
for coins in response.portfolio.bank_balances:
  print("\tcoin:", coins.amount, coins.denom)

print("portfolio subaccount balances:")
for subaccount in response.portfolio.subaccounts:
  print(
    "\tsubaccount:",
    subaccount.subaccount_id,
    subaccount.deposit.available_balance, "/", subaccount.deposit.available_balance,
    subaccount.denom,
  )
```

| Name | Type | Description |
| - | - | - |
| `portfolio` | `Portfolio` | Your account portfolio |
