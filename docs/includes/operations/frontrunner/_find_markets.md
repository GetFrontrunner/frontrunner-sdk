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

<aside class="notice">
The response values aside from <code>market_ids</code> and <code>markets</code> is for debugging. Except for markets, if there are not sufficient constraints, the response fields may contain values unrelated to the final set of markets ie. if your only constraint is for the Seattle Mariners (baseball) team, leagues will contain values for all sports (including baseball).
</aside>

| Name | Type | Description |
| - | - | - |
| `league_ids` | `[str]` | Related sport league IDs, from `sports` and `league_names` constraints |
| `leagues` | `[League]` | Related sport league objects |
| `sport_event_ids` | `[str]` | Related sport event IDs, from leagues and `event_types` constraints |
| `sport_events` | `[SportEvent]` | Related sport event objects |
| `sport_entity_ids` | `[str]` | Related sport entity IDs, from leagues and entity names/abbreviations constraints |
| `sport_entities` | `[SportEntity]` | Related sport entity objects |
| `prop_ids` | `[str]` | Related proposition IDs, from leagues, sport events, and `prop_types` constraints |
| `props` | `[Prop]` | Related proposition objects |
| `market_ids` | `[str]` | Related market IDs, from sport entities, props, and `market_statuses` constraints |
| `markets` | `[Market]` | Related market objects |
