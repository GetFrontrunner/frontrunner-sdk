## Injective: Get Order Books

Gets the order books for specific markets. For the corresponding Injective API, see [Order Books v2][order-books-v2].

[order-books-v2]: https://api.injective.exchange/#injectivederivativeexchangerpc-orderbooksv2

### Parameters

```python
market_id = "0xd5e4b12b19ecf176e4e14b42944731c27677819d2ed93be4104ad7025529c7ff"

# Get order books for given market ids
response = sdk.injective.get_order_books([market_id])
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `market_ids` | `[str]` | ✓ | IDs of markets to look up orders for |

### Response

```python
print("order_books:")
for market_id, order_book in response.order_books.items():
  print("\tmarket:", market_id)

  for buy in order_book.buys:
    print("\t\tbuy:", buy.quantity, "@", buy.price)

  for sell in order_book.sells:
    print("\t\tsell:", sell.quantity, "@", sell.price)
```

| Name | Type | Description |
| - | - | - |
| `order_books` | `Mapping[str, DerivativeLimitOrderbookV2]` | Order books keyed by market ID |
