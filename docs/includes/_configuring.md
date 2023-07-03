# Configuring

## SDK Parameters

There are a few ways to configure values for the SDK. In order of precedence, they are as follows:

1. Direct named environment variables
2. Presets via environment variables
3. Default values

## Wallet

This specifies which wallet the SDK will use for mutating the blockchain and querying the blockchain for "my" data. These variables are checked in order.

### Environment Variables

1. `FR_WALLET_MNEMONIC`
1. `FR_WALLET_PRIVATE_KEY_HEX`

### Default

`None`

## Frontrunner Base API URL

This is the base URL for Frontrunner-specific operations such as finding markets.

### Environment Variables

* `FR_PARTNER_API_BASE_URL`

### Default

`https://partner-api-testnet.getfrontrunner.com/api/v1`

## Frontrunner API Token

To interact with the Frontrunner APIs, you will need a token to authenticate. Requests without authentication will fail.

### Environment Variable

* `FR_PARTNER_API_TOKEN`

### Default

`None`

## Injective Network

The "network" is which blockchain network to use. Valid values are...

* `testnet`
* `mainnet`

For testing with "play" money and developing code, use `testnet`. For production and "real" money, use `mainnet`.

The chain ID must match with the Injective network you are using.

| Network | Chain ID |
| - | - |
| testnet | injective-888 |
| mainnet | injective-1 |

### Environment Variable

* `FR_INJECTIVE_NETWORK`
* `FR_INJECTIVE_CHAIN_ID`

### Default

Network is `testnet`, and Chain ID is `injective-888`.

## Injective Endpoints

Injective is built on the Cosmos network. Cosmos defines a set of well known endpoint types that are supported for interacting with the blockchain. You can learn more about them here: [Cosmos Good-To-Know Dev Terms][cosmos-terminology].

[cosmos-terminology]: https://tutorials.cosmos.network/tutorials/1-tech-terms/

In Cosmos, we have the following endpoints:

* Exchange
* Explorer
* Light Client Daemon (LCD)
* Remote Procedure Call (RPC)
* Google RPC (gRPC)

Normally, these come in sets, and are not interchangeable between sets.

<aside class="notice">
Some endpoints are specified as an <a href="https://en.wikipedia.org/wiki/Uniform_Resource_Identifier#Syntax">authority (host + port)</a>, and some are specified as a base URL.
</aside>

### Environment Variables

* `FR_INJECTIVE_EXCHANGE_AUTHORITY`
* `FR_INJECTIVE_EXPLORER_AUTHORITY`
* `FR_INJECTIVE_LCD_BASE_URL`
* `FR_INJECTIVE_RPC_BASE_URL`
* `FR_INJECTIVE_GRPC_AUTHORITY`

### Defaults

Frontrunner does not run the Injective Explorer, so Explorer Authority defaults are always Injective's.

### Testnet

| Endpoint Type | Default Value |
| - | - |
| Exchange Authority | `injective-node-testnet.grpc-exchange.getfrontrunner.com:443` |
| Explorer Authority | `k8s.testnet.explorer.grpc.injective.network:443` |
| LCD Base URL | `https://injective-node-testnet.lcd.getfrontrunner.com` |
| RPC Base URL | `wss://injective-node-testnet.tm.getfrontrunner.com/websocket` |
| gRPC Authority | `injective-node-testnet.grpc.getfrontrunner.com:443` |

### Mainnet

| Endpoint Type | Default Value |
| - | - |
| Exchange Authority | `injective-node-mainnet.grpc-exchange.getfrontrunner.com:443` |
| Explorer Authority | `k8s.global.mainnet.explorer.grpc.injective.network:443` |
| LCD Base URL | `https://injective-node-mainnet.lcd.getfrontrunner.com` |
| RPC Base URL | `wss://injective-node-mainnet.tm.getfrontrunner.com/websocket` |
| gRPC Authority | `injective-node-mainnet.grpc.getfrontrunner.com:443` |

### Presets

The preset endpoint groups for Injective are taken from Injective's
`Network` class [here](https://github.com/InjectiveLabs/sdk-python/blob/master/pyinjective/constant.py).

#### Injective Testnet K8s
When the environment variable `FR_PRESET_NODES` is set to `injective-k8s` and the SDK is configured for `testnet`,
Injective's Kubernetes-based endpoints on the testnet network (`Network.testnet()`) will be used instead of the defaults above.

#### Injective Mainnet Global
When the environment variable `FR_PRESET_NODES` is set to `injective-global` and the SDK is configured for `mainnet`,
Injective's global, load-balanced endpoints on the mainnet network (`Network.mainnet("lb")`) will be used.

#### Injective Mainnet Sentry
When the environment variable `FR_PRESET_NODES` is set to `injective-sentry` and the SDK is configured for `mainnet`,
one of Injective's standalone sentry nodes on the mainnet network (`Network.mainnet("sentry0")`) will be used.

## Injective Faucet

A [faucet][faucet] is a site that dispenses free tokens to a wallet. Faucets are used to acquire tokens without involving "real" money or mining them yourself.  
This faucet is only relevant for `testnet` - there is no faucet on mainnet.

[faucet]: https://coinmarketcap.com/alexandria/article/what-is-a-crypto-faucet

### Environment Variable

* `FR_INJECTIVE_FAUCET_BASE_URL`

### Default

`https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI`

## Configuring Logging

All actions within the SDK are logged via Python's `logging` module. The `logging` module is hierarchical, so you can selectively turn off sections of a module by name.

```python
import logging

# Set logging for frontrunner-sdk to INFO and above
logging.getLogger("frontrunner_sdk").setLevel(logging.INFO)

# Only log critical errors from config and clients
logging.getLogger("frontrunner_sdk.clients").setLevel(logging.CRITICAL)
logging.getLogger("frontrunner_sdk.config").setLevel(logging.CRITICAL)
```

The default logging level is the same as `logging`'s defaults.

For more information on configuring Python's logging, see the [Python Logging Cookbook][logging-cookbook].

[logging-cookbook]: https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook
