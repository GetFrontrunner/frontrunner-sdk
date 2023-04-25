from dataclasses import dataclass
from functools import cached_property
from typing import Optional

from pyinjective import Address
from pyinjective import PrivateKey
from pyinjective import PublicKey


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
