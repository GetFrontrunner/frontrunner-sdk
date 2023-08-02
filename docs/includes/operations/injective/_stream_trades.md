## Injective: Stream Trades

Get new trades as they arrive. For the corresponding Injective API, see [Stream Trades][stream-trades].

[stream-trades]: https://api.injective.exchange/#injectivespotexchangerpc-streamtrades

<aside class="notice">
This operation only exists in the <code>async</code> SDK.
</aside>

### Parameters

```python
async def run():
  market_id = "0x90e662193fa29a3a7e6c07be4407c94833e762d9ee82136a2cc712d6b87d7de3"

  response = async_sdk.injective.stream_trades(market_id)
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `market_id` | `str` | ✓ | Market ID to watch for orders |
| `mine` | `bool` | ◯ `False` | Only watch for my orders |
| `subaccount` | `Subaccount` | ◯ `None` | Only return orders from this subaccount. |
| `subaccount_index` | `int` | ◯ `None` | Only return orders from this subaccount index of your wallet. Sets `mine=True` |
| `subaccounts` | `[Subaccount]` | ◯ `None` | Only return orders from these subaccounts. |
| `subaccount_indexes` | `[int]` | ◯ `None` | Only return orders from these subaccount indexes of your wallet. Sets `mine=True` |
| `direction` | `"buy", "sell"` | ◯ `None` | Only watch for orders of this direction |
| `side` | `"maker", "taker"` | ◯ `None` | Only watch for orders of this side |

### Response

```python
async def run():
  response = async_sdk.injective.stream_trades(market_id)

  async for trade in response.trades:
    print("trade:", trade.operation_type, trade.trade.order_hash)
```

| Name | Type | Description |
| - | - | - |
| `trades` | `AsyncIterator[DerivativeTrade]` | Iterator for trades |
