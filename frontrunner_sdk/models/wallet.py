from dataclasses import dataclass
from functools import cached_property

from pyinjective import Address
from pyinjective import PrivateKey
from pyinjective import PublicKey


@dataclass(frozen=True)
class Wallet:
  mnemonic: str
  private_key: PrivateKey

  @cached_property
  def public_key(self) -> PublicKey:
    return self.private_key.to_public_key()

  @cached_property
  def address(self) -> Address:
    return self.public_key.to_address()

  @cached_property
  def ethereum_address(self) -> str:
    return "0x" + self.address.to_hex()

  @cached_property
  def injective_address(self) -> str:
    return self.address.to_acc_bech32()

  def subaccount_address(self, index: int = 0) -> str:
    return self.address.get_subaccount_id(index)

  @cached_property
  def sequence(self) -> str:
    return self.address.get_sequence()

  @cached_property
  def account_number(self) -> str:
    return self.address.get_number()

  @classmethod
  def _new(clz):
    mnemonic, private_key = PrivateKey.generate()
    return clz(mnemonic=mnemonic, private_key=private_key)

  @classmethod
  def _from_mnemonic(clz, mnemonic: str):
    private_key = PrivateKey.from_mnemonic(mnemonic)
    return clz(mnemonic=mnemonic, private_key=private_key)
