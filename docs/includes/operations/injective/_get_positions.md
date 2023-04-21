## Injective: Get Positions

Gets open positions. For the corresponding Injective API, see [Positions][derivative-positions].

[derivative-positions]: https://api.injective.exchange/#injectivederivativeexchangerpc-positions

### Parameters

```python
market_id = "0x90e662193fa29a3a7e6c07be4407c94833e762d9ee82136a2cc712d6b87d7de3"

# Get all buy positions
response = sdk.injective.get_positions(
  [market_id],
  direction="buy",
)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `market_ids` | `[str]` | ✓ | IDs of markets to look up positions for |
| `mine` | `bool` | ◯ `False` | Only find positions for this wallet |
| `direction` | `"buy", "sell"` | ◯ `None` | Only find positions with this direction |
| `start_time` | `datetime` | ◯ `None` | Only find positions executing on or after this time |
| `end_time` | `datetime` | ◯ `None` | Only find positions executing on or before this time |

### Response

```python
print("positions:", response.positions)
```

| Name | Type | Description |
| - | - | - |
| `positions` | `[DerivativePosition]` | Positions for the given markets |
