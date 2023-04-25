## Injective: Stream Positions

Get new positions as they arrive. For the corresponding Injective API, see [Stream Positions][stream-positions].

[stream-positions]: https://api.injective.exchange/#injectivederivativeexchangerpc-streampositions

<aside class="notice">
This operation only exists in the <code>async</code> SDK.
</aside>

### Parameters

```python
async def run():
  response = async_sdk.injective.stream_positions()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `mine` | `bool` | ◯ | Only stream positions that are mine |
| `market_ids` | `[str]` `None` | ◯ | Only stream positions for the given markets |
| `subaccount_ids` | `[str]` `None` | ◯ | Only stream positions that are from the given subaccount |

### Response

```python
async def run():
  response = ...

  async for position in response.positions:
    print(
      "position:",
      position.ticker,
      position.direction,
      position.quantity, "@", position.entry_price,
    )
```

| Name | Type | Description |
| - | - | - |
| `positions` | `AsyncIterator[DerivativePosition]` | Iterator for positions |
