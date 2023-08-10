# Gas and Fees

Gas represents the computational effor required to execute an operation. The fee is how much `INJ` to pay to execute a transaction. Insufficient gas will result in a failed transaction, and consumed gas.

The fee amount is `fee = gas * gas price` where `gas price` is an arbitrary constant.

To learn more, see [Gas and Fees][gas-and-fees] from the Injective and Cosmos documentation.

[gas-and-fees]: https://docs.injective.network/learn/basic-concepts/gas_and_fees/

## Gas Estimation

Injective docs suggest using simulation to estimate the amount of gas required to execute a specific transaction. However, simulation is slow (around 2 seconds). For HFT use cases, this SDK uses a precomputed lookup table to estimate the required gas. Because of the way the underlying Cosmos SDK works, gas is strongly tied to the size of the message and is also time-independent. That property allows us to roughly estimate the amount of gas to send based on the type of message and number of orders it contains.

To ensure there is enough gas, and to account for errors in estimation, a flat gas "buffer" amount is also added.

For HFT and API trading notes, see [this Injective note][note-for-hft-api-traders].

[note-for-hft-api-traders]: https://api.injective.exchange/#derivatives-localorderhashcomputation
