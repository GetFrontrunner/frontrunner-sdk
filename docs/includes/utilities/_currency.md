## Currency

Injective operates on raw coin quantities instead of decimal values. For example, 8 FRCOIN (as well as USDC and USDT) would be represented as `"8000000"`. This is because FRCOIN's denomination is to 6 decimal places, and 8 shifted by 6 decimal places is 8,000,000.

Each denomination has its own fractional resolution, and all are mapped in Injective's SDK. See:

* [devnet](https://github.com/InjectiveLabs/sdk-python/blob/master/pyinjective/denoms_devnet.ini)
* [testnet](https://github.com/InjectiveLabs/sdk-python/blob/master/pyinjective/denoms_testnet.ini)
* [mainnet](https://github.com/InjectiveLabs/sdk-python/blob/master/pyinjective/denoms_mainnet.ini)

Also, denominations are usually returned as their peggy identity. These identities aren't easily human-interpretable and vary between devnet, testnet, and mainnet.

To make working with Injective's units easier, this SDK includes methods to get a unified representation of `Currency` without needing to know denomination details such as how many digits of precision are involved.

In `Currency` terms, `quantity` means the Injective-side raw (decimal-less) value and `value` means the human-friendly value (with decimals).

### From Value

Factory for `Currency`, given the Injective-side quantity and denomination.

#### Example

```python
currency = sdk.utilities.currency_from_quantity(420_690_000, "FRCOIN")
print(
  "currency:",
  "[", currency.value, currency.denom.name, "]",
  "is represented as",
  "[", currency.quantity, currency.denom.peggy, "]",
  "in injective",
)
```

#### Parameters

| Name | Type | Req? | Description |
| - | - | - | - |
| `quantity` | `int, str` | ✓ | Injective-side coin quantity |
| `denom_name` | `str` | ✓ | Name of denomination (human-readable name or peggy identity) |

#### Returns

A currency object.

### From Quantity

Factory for `Currency`, given the human-readable quantity and denomination.

#### Example

```python
currency = sdk.utilities.currency_from_value(420.69, "FRCOIN")
print(
  "currency:",
  "[", currency.value, currency.denom.name, "]",
  "is represented as",
  "[", currency.quantity, currency.denom.peggy, "]",
  "in injective",
)
```

#### Parameters

| Name | Type | Req? | Description |
| - | - | - | - |
| `value` | `int, str` | ✓ | Human-readable coin value |
| `denom_name` | `str` | ✓ | Name of denomination (human-readable name or peggy identity) |

#### Returns

A currency object.
