## Frontrunner: Get Props

Get Frontrunner props. 

### Parameters

```python
# Get all NFL props
league_id = "c6c521c4-88d0-463d-aa2a-fe3765ec872a"
response = sdk.frontrunner.get_props(
    league_id=league_id,
)

# Get all Frontrunner props
response = sdk.frontrunner.get_props()
```

| Name | Type | Req? | Description |
| - | - | - | - |
| `id` | `str` | ◯ | Only include the specific prop |
| `league_id` | `str` | ◯ | Only include the props for the given league |

### Response

```python
print(f"Props: {response.props}")
```

| Name | Type | Description |
| - | - | - |
| `props` | `[Prop]` | Related prop objects |
