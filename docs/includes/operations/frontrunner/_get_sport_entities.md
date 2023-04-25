## Frontrunner: Get Sport Entitiees

Get Frontrunner sport entities (i.e. teams, players, etc.) 

### Parameters

```python
# Get all NFL sport entities
league_id = "c6c521c4-88d0-463d-aa2a-fe3765ec872a"
response = sdk.frontrunner.get_sport_entities(
    league_id=league_id,
)

# Get all Frontrunner sport entities
response = sdk.frontrunner.get_sport_entities()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `id` | `str` | ◯ | Only include the specific sport entity |
| `league_id` | `str` | ◯ | Only include the sport entities for the given league |
| `sport` | `str` | ◯ | Only include the sport entities for the given sport |

### Response

```python
print(f"Sport Entities: {response.sport_entities}")
```

| Name | Type | Description |
| - | - | - |
| `sport_entities` | `[SportEntity]` | Related sport entity objects |
