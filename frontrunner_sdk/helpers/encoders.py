import base64


def b64_to_hex(b64_value: str) -> str:
  return base64.b64decode(b64_value.encode("utf-8")).hex()


def hex_to_b64(hex_value: str) -> str:
  return str(base64.b64encode(bytes.fromhex(hex_value)), "utf-8")
