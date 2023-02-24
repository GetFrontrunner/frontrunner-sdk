import os
import sys
import json
from typing import Dict
import requests
from pyinjective.wallet import PrivateKey, Address
from utils import set_env_variables, check_env_is_on


### Generate and Fund an Injective Wallet

# 1. `python examples/generate_account.py`. This creates a new Injective wallet funded with INJ and USDT and logs the private key, mnemonic, Injective address, and Ethereum address. **Store this somewhere secure to reuse for future tests**.
# 2. Export shell environment variables
#    1. `export INJ_ADDRESS=<inj_address_from_above>`
#    2. `export INJ_PRIVATE_KEY=<inj_private_from_above>`
# 3. Request testnet INJ and USDT via Injective’s testnet faucet
#    1. `curl -X POST [https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI?address=](https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI?address=inj1sx0f8xdm39plu57095tvztly4lr0h7vfhfmhqt)$INJ_ADDRESS`
#    2. If the above doesn’t work, input the address here: [https://testnet.faucet.injective.network/](https://testnet.faucet.injective.network/)

env_name_1 = "INJ_ADDRESS"
env_name_2 = "INJ_PRIVATE_KEY"


def generate_mnemonic() -> Dict[str, str]:
    mnemonic, privkey = PrivateKey.generate()
    inj_address = privkey.to_public_key().to_address().to_acc_bech32()
    secret_obj = {
        "mnemonic": mnemonic,
        "inj_private_key": privkey.to_hex(),
        "inj_address": inj_address,
        "eth_address": get_eth_address_from_inj(inj_address),
    }
    print(f"Generated Injective wallet:\n{json.dumps(secret_obj, indent=2)}")
    return secret_obj


def get_eth_address_from_inj(inj_wallet_address: str) -> str:
    address = Address.from_acc_bech32(inj_wallet_address)
    eth_address = address.get_ethereum_address()
    print(f"Got '{eth_address=}' from '{inj_wallet_address=}'")
    return eth_address


def request_test_tokens(inj_address: str):
    print("requesting test tokens(this may take several seconds)")
    response = requests.post(
        f"https://knroo5qf2e.execute-api.us-east-2.amazonaws.com/default/TestnetFaucetAPI?address={inj_address}"
    )
    if response.status_code != 200:
        print("failed to request test token")
        print("please request your test tokens from: https://testnet.faucet.injective.network")
    else:
        print("succeeded in requesting test tokens")


def main(file_location: str):
    secret_obj = generate_mnemonic()

    set_env_variables(secret_obj, file_location)

    for key in ("inj_address", "inj_private_key"):
        check_env_is_on(key.upper())

    os.system(f"bash -c 'cat {file_location}'")
    os.system(f"bash -c 'source {file_location}'")

    request_test_tokens(secret_obj["inj_address"])
    print("run 'source .env' to set env variables")


if __name__ == "__main__":
    file_location = "examples.env"
    main(file_location)
