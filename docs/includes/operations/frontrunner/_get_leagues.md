## Frontrunner: Get Leagues

Get Frontrunner leagues. 

### Parameters

```python
# Get all Frontrunner leagues
response = sdk.frontrunner.get_leagues()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `id` | `str` | ◯ | Only include the specific league |
| `sport` | `str` | ◯ | Only include the leagues for the given sport |

### Response

```python
print(f"Leagues: {response.leagues}")
```

| Name | Type | Description |
| - | - | - |
| `leagues` | `[League]` | Related league objects |
