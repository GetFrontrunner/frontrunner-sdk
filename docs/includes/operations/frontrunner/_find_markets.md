## Frontrunner: Find Markets

Enhanced search of Frontrunner markets.

<aside class="notice">
This operation is a convenience search function built on top of a combination of Frontrunner API calls.
The other Frontrunner operations map 1:1 to the Frontrunner REST API endpoints.
</aside>


### Parameters

```python
# Find Frontrunner markets where...
response = sdk.frontrunner.find_markets(
  # ...the winner
  prop_type=["winner"],
  # ...of a basketball
  sports=["basketball"],
  # ...game
  event_types=["game"],
  # ...is the Los Angeles Lakers (LAL)
  sport_entity_abbreviations=["LAL"],
)

# Find Frontrunner markets where...
response = sdk.frontrunner.find_markets(
  # ...formula one
  sports=["formula1"],
  # ...team Williams or Alfa Romeo
  sport_entity_names=["Williams", "Alfa Romeo"],
  # ...is not for a 'winner' type prop
  prop_types=["other"],
)

# Get all active Frontrunner markets
response = sdk.frontrunner.find_markets()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `sports` | `[str]` | ◯ | Only include the given sports |
| `league_names` | `[str]` | ◯ | Only include the given league names |
| `event_types` | `[str]` | ◯ | Only include the given event types; must be in `[game, future]` |
| `sport_entity_names` | `[str]` | ◯ | Only include the given entity names (eg. Atlanta Hawks) |
| `sport_entity_abbreviations` | `[str]` | ◯ | Only include the given entity abbreviations (eg. ATL) |
| `prop_types` | `[str]` | ◯ | Only include the given prop types; must be in `[winner, other]` |
| `market_statuses` | `[str]` | ◯ | Only include the given market statuses; must be in `[active, closed]` |

### Response

```python
for market in response.markets:
    print(f"Market: {market.address} [{market.long_entity_name} / {market.short_entity_name}]")
```

| Name | Type | Description |
| - | - | - |
| `market_ids` | `[str]` | Related market IDs, from sport entities, props, and `market_statuses` constraints |
| `markets` | `[Market]` | Related market objects |
