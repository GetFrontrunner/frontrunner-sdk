## Frontrunner: Get Sport Events

Get Frontrunner sport events

### Parameters

```python
# Get all NFL sport events
league_id = "c6c521c4-88d0-463d-aa2a-fe3765ec872a"
response = sdk.frontrunner.get_sport_events(
    league_id=league_id,
)

# Get all Frontrunner sport events
response = sdk.frontrunner.get_sport_events()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `id` | `str` | ◯ | Only include the specific sport event |
| `league_id` | `str` | ◯ | Only include the sport events for the given league |
| `sport` | `str` | ◯ | Only include the sport events for the given sport |
| `starts_since` | `datetime` | ◯ | Only include the sport events starting after the given datetime |

### Response

```python
print(f"Sport Events: {response.sport_events}")
```

| Name | Type | Description |
| - | - | - |
| `sport_events` | `[SportEvent]` | Related sport event objects |
