# Configuring

## Ways to Configure SDK Parameters

There are a few ways to configure values for the SDK. In order of precedence, they are as follows:

1. Direct named environment variables
2. Presets via environment variables
3. Default values

## Parameter Configuration: Wallet

This specifies which wallet the SDK will use for mutating the blockchain and querying the blockchain for "my" data. These variables are checked in order.

### Environment Variables

1. `FRONTRUNNER_WALLET_MNEMONIC`
1. `FRONTRUNNER_WALLET_PRIVATE_KEY_HEX`

### Default

`None`

## Parameter Configuration: Frontrunner Base API URL

This is the base URL for Frontrunner-specific operations such as finding markets.

### Environment Variables

* `FRONTRUNNER_FRONTRUNNER_API_BASE_URL`

### Default

`https://partner-api-staging.getfrontrunner.com/api/v1`

## Parameter Configuration: Frontrunner API Token

To interact with the Frontrunner APIs, you will need a token to authenticate. Requests without authentication will fail.

### Environment Variable

* `FRONTRUNNER_FRONTRUNNER_API_AUTHN_TOKEN`

### Default

`None`

## Parameter Configuration: Injective Network

The "network" is which blockchain network to use. Valid values are...

* `devnet`
* `testnet`
* `mainnet`

For testing with "play" money and developing code, use `testnet`. For production and "real" money, use `mainnet`.

The chain ID must match with the Injective network you are using.

| Network | Chain ID |
| - | - |
| devnet | injective-777 |
| testnet | injective-888 |
| mainnet | injective-1 |

### Environment Variable

* `FRONTRUNNER_INJECTIVE_NETWORK`
* `FRONTRUNNER_INJECTIVE_CHAIN_ID`

### Default

Network is `testnet`, and Chain ID is `injective-888`.

## Parameter Configuration: Injective Endpoints

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
Some endpoints are specified as an authority, and some are specified as a base URL.
</aside>

### Environment Variables

* `FRONTRUNNER_INJECTIVE_EXCHANGE_AUTHORITY`
* `FRONTRUNNER_INJECTIVE_EXPLORER_AUTHORITY`
* `FRONTRUNNER_INJECTIVE_LCD_BASE_URL`
* `FRONTRUNNER_INJECTIVE_RPC_BASE_URL`
* `FRONTRUNNER_INJECTIVE_GRPC_AUTHORITY`

### Presets

Environment Variable `FRONTRUNNER_PRESET_NODES` is `injective`. This will use Injective's Kubernetes-based nodes on the testnet network.

| Endpoint Type | Default Value |
| - | - |
| Exchange Authority | `k8s.testnet.exchange.grpc.injective.network:443` |
| Explorer Authority | `k8s.testnet.explorer.grpc.injective.network:443` |
| LCD Base URL | `https://k8s.testnet.lcd.injective.network` |
| RPC Base URL | `wss://k8s.testnet.tm.injective.network/websocket` |
| gRPC Authority | `k8s.testnet.chain.grpc.injective.network:443` |

### Defaults

| Endpoint Type | Default Value |
| - | - |
| Exchange Authority | `injective-node-v2-staging.grpc-exchange.getfrontrunner.com:443` |
| Explorer Authority | `injective-node-v2-staging.grpc-explorer.getfrontrunner.com:443` |
| LCD Base URL | `https://injective-node-v2-staging.lcd.getfrontrunner.com` |
| RPC Base URL | `wss://injective-node-v2-staging.tm.getfrontrunner.com/websocket` |
| gRPC Authority | `injective-node-v2-staging.grpc.getfrontrunner.com:443` |

## Parameter Configuration: Injective Faucet

A [faucet][faucet] is a site that dispenses free tokens to a wallet. Faucets are used to acquire tokens without involving "real" money or mining them yourself.

[faucet]: https://coinmarketcap.com/alexandria/article/what-is-a-crypto-faucet

### Environment Variable

* `FRONTRUNNER_INJECTIVE_FAUCET_BASE_URL`

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