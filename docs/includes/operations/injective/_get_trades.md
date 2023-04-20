## Injective: Get Trades

Gets open positions. For the corresponding Injective API, see [Trades][derivative-trades].

[derivative-trades]: https://api.injective.exchange/#injectivederivativeexchangerpc-trades

### Parameters

```python
market_id = "0x90e662193fa29a3a7e6c07be4407c94833e762d9ee82136a2cc712d6b87d7de3"

# Get all trades on the maker side
response = sdk.injective.get_trades(
  [market_id],
  side="maker",
)
```

| Name | Type | | Description |
| - | - | - | - |
| `market_ids` | `[str]` | ✓ | IDs of markets to look up trades for |
| `mine` | `bool` | ◯ `False` | Only find trades for this wallet |
| `direction` | `"buy", "sell"` | ◯ `None` | Only find trades with this direction |
| `side` | `"maker", "taker"` | ◯ `None` | Only find trades with this side |
| `start_time` | `datetime` | ◯ `None` | Only find trades executing on or after this time |
| `end_time` | `datetime` | ◯ `None` | Only find trades executing on or before this time |

### Response

```python
print("trades:", response.trades)
```

| Name | Type | Description |
| - | - | - |
| `trades` | `[DerivativeTrade]` | Trades for the given markets |
