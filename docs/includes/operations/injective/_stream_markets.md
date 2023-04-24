## Injective: Stream Markets

Get market updates as they arrive. For the corresponding Injective API, see [Stream Markets][stream-markets].

[stream-markets]: https://api.injective.exchange/#injectivederivativeexchangerpc-streammarkets

<aside class="notice">
This operation only exists in the <code>async</code> SDK.
</aside>

### Parameters

```python
async def run():
  market_id = "0x90e662193fa29a3a7e6c07be4407c94833e762d9ee82136a2cc712d6b87d7de3"

  response = async_sdk.injective.stream_markets([market_id])
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `market_ids` | `[str]` | ✓ | Market IDs to watch for updates |

### Response

```python
async def run():
  response = ...

  async for market in response.markets:
      print(market)
```

| Name | Type | Description |
| - | - | - |
| `markets` | `AsyncIterator[DerivativeMarketInfo]` | Iterator for market updates |
