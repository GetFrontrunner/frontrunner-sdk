import re

from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from pyinjective import Address
from pyinjective import PrivateKey
from pyinjective import PublicKey

from frontrunner_sdk.exceptions import FrontrunnerArgumentException

SUBACCOUNT_REGEX = re.compile("^0x[0-9a-fA-F]{64}$") # Injective regex
ETHEREUM_ADDRESS_REGEX = re.compile("^0x[0-9a-fA-F]{40}$")


def is_valid_subaccount(subaccount_id):
  return SUBACCOUNT_REGEX.match(subaccount_id)


def is_valid_ethereum_address(wallet_address: str):
  return ETHEREUM_ADDRESS_REGEX.match(wallet_address)


@dataclass(frozen=True, repr=False)
class Wallet:
  private_key: PrivateKey
  mnemonic: Optional[str] = None

  @cached_property
  def public_key(self) -> PublicKey:
    return self.private_key.to_public_key()

  @cached_property
  def address(self) -> Address:
    return self.public_key.to_address()

  @property
  def ethereum_address(self) -> str:
    return "0x" + self.address.to_hex()

  @property
  def injective_address(self) -> str:
    return self.address.to_acc_bech32()

  def subaccount_address(self, index: int = 0) -> str:
    return self.address.get_subaccount_id(index)

  @property
  def sequence(self) -> int:
    return self.address.sequence

  def get_and_increment_sequence(self) -> int:
    return self.address.get_sequence()

  @property
  def account_number(self) -> int:
    return self.address.number

  @classmethod
  def _new(clz):
    mnemonic, private_key = PrivateKey.generate()
    return clz(mnemonic=mnemonic, private_key=private_key)

  @classmethod
  def _from_mnemonic(clz, mnemonic: str):
    private_key = PrivateKey.from_mnemonic(mnemonic)
    return clz(mnemonic=mnemonic, private_key=private_key)

  @classmethod
  def _from_private_key(clz, private_key_hex: str):
    private_key = PrivateKey.from_hex(private_key_hex)
    return clz(private_key=private_key)


@dataclass(frozen=True)
class Subaccount:
  subaccount_id: str
  address: Address

  @property
  def ethereum_address(self) -> str:
    return "0x" + self.address.to_hex()

  @property
  def injective_address(self) -> str:
    return self.address.to_acc_bech32()

  @classmethod
  def from_wallet_and_index(clz, wallet: Wallet, index: int):
    address = wallet.address
    return clz(wallet.subaccount_address(index), address)

  @classmethod
  def from_injective_address_and_index(clz, injective_address: str, index: int):
    address = Address.from_acc_bech32(injective_address)
    return clz(address.get_subaccount_id(index), address)

  @classmethod
  def from_ethereum_address_and_index(clz, ethereum_address: str, index: int):
    if not is_valid_ethereum_address(ethereum_address):
      raise FrontrunnerArgumentException(
        f"Provided address '{ethereum_address}' is invalid. Does not match {ETHEREUM_ADDRESS_REGEX}"
      )
    hex_bytes = bytes.fromhex(ethereum_address.replace("0x", ""))
    address = Address(hex_bytes)
    return clz(address.get_subaccount_id(index), address)

  @classmethod
  def from_subaccount_id(clz, subaccount_id: str):
    if not is_valid_subaccount(subaccount_id):
      raise FrontrunnerArgumentException(
        f"Provided subaccount '{subaccount_id}' is invalid. Does not match {SUBACCOUNT_REGEX}"
      )
    hex_bytes = bytes.fromhex(subaccount_id[:-24].replace("0x", ""))
    address = Address(hex_bytes)
    return clz(subaccount_id, address)
