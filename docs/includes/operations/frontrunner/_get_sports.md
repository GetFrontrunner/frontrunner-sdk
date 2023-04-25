## Frontrunner: Get Sports

Get supported sports on Frontrunner

### Parameters

```python
# Get all Frontrunner sports
response = sdk.frontrunner.get_sports()
```

No parameters. Note that this is convenience operation that collects all sports from `get_leagues`.

### Response

```python
print(f"Sports: {response.sports}")
```

| Name | Type | Description |
| - | - | - |
| `sports` | `[str]` | All sport names |
