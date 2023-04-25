## Frontrunner: Find Markets

Find Frontrunner markets with specific criteria.

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
