# Conventions

## Response Objects

SDK return values are always wrapped in a response object. The response object contains the desired values eg. orders, positions, portfolio info. This is to mitigate the effects of SDK changes for developers.

```python
sdk = FrontrunnerSDK()

# SDK return values are always response objects
response = sdk.injective.some_list_operation()

# Desired values will be Within the response object
desired_value = response.desired_value
maybe_other_value = response.maybe_other_value
```

## API Namespaces

Within the SDK, we split the operations into the following namespaces:

* Frontrunner
* Injective

This split exists so that the origin of the call data is transparent. For example, if you only wish to interact with Frontrunner services, only use the calls available in the `frontrunner` namespace in the SDK.

## Exceptions

In general, this SDK wraps downstream exceptions in our own exception classes. Also, each exception class has a specific meaning.

| Class | Meaning |
| - | - |
| `FrontrunnerException` | Root exception for anything raised by this SDK |
| `FrontrunnerUserException` | User is at fault |
| `FrontrunnerExternalException` | User is _not_ at fault |
| `FrontrunnerConfigurationException` | User did not configure or misconfigured a value required by the SDK |
| `FrontrunnerArgumentException` | User provided an invalid value to an operation |
| `FrontrunnerInjectiveException` | User provided an invalid value to an Injective API |
| `FrontrunnerUnserviceableException` | Service is not usable eg. responds with 5xx status code |

## Logging

All actions within the SDK are logged via Python's `logging` module. Each log level has a specific meaning.

`CRITICAL` logs indicate that the SDK cannot function. Examples include unreachable endpoints, inoperable endpoints, incorrect credentials, and system errors. Typically, these are logged alongside a raised `FrontrunnerExternalException`.

`ERROR` logs are generated alongisde every raised exception ie. `logger.exception(...)`.

`WARNING` logs indicate a given operation, parameter, or configuration is deprecated, and should not be used. The warning will include an alternative to use.

`INFO` logs are generated after every completed SDK operation. These logs serve as an audit trail of what happened in the SDK.

`DEBUG` logs are generated around (before + after) every external API call, before calling an external process, and after configuration is read. With debug logs, there should be enough detail to recreate the sequence of events that lead to a specific failure at the SDK level.
