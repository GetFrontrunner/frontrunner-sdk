## Frontrunner: Get Markets

Get Frontrunner markets. 

### Parameters

```python
from frontrunner_sdk.openapi.frontrunner_api import MarketStatus

# Get all active NFL markets
league_id = "c6c521c4-88d0-463d-aa2a-fe3765ec872a"
response = sdk.frontrunner.get_markets(
    league_id=league_id,
    status=MarketStatus.ACTIVE,
)

# Get all active Frontrunner markets
response = sdk.frontrunner.get_markets()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `id` | `str` | ◯ | Only include the specific market |
| `injective_id` | `str` | ◯ | Only include the market corresponding to the given Injective market |
| `prop_id` | `str` | ◯ | Only include markets for the given prop |
| `event_id` | `str` | ◯ | Only include markets for the given event |
| `league_id` | `str` | ◯ | Only include markets for the given league |
| `status` | `str` | ◯ | Only include the given market status; must be one of `[active, closed]` |

### Response

```python
for market in response.markets:
    print(f"Market: {market.address} [{market.long_entity_name} / {market.short_entity_name}]")
```

| Name | Type | Description |
| - | - | - |
| `markets` | `[Market]` | Related market objects |
