from dataclasses import dataclass
from functools import cached_property

from pyinjective import PrivateKey


@dataclass(frozen=True)
class Wallet:
  mnemonic: str
  private_key: PrivateKey

  @cached_property
  def public_key(self) -> str:
    return "0x" + self.private_key.to_public_key().to_hex()

  @cached_property
  def ethereum_address(self) -> str:
    return "0x" + self.private_key.to_public_key().to_address().to_hex()

  @cached_property
  def injective_address(self) -> str:
    return self.private_key.to_public_key().to_address().to_acc_bech32()

  @classmethod
  def new(clz):
    mnemonic, private_key = PrivateKey.generate()
    return clz(mnemonic=mnemonic, private_key=private_key)

  @classmethod
  def from_mnemonic(clz, mnemonic: str):
    private_key = PrivateKey.from_mnemonic(mnemonic)
    return clz(mnemonic=mnemonic, private_key=private_key)
