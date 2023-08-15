from unittest import TestCase

from frontrunner_sdk.helpers.encoders import b64_to_hex, hex_to_b64


class TestEncoders(TestCase):

  def test_b64_to_hex(self):
    self.assertEqual(
      "b2195542938e1b2f8601df0509b8e56b1c7b2f049e6efb996e799cffa2d5e517",
      b64_to_hex("shlVQpOOGy+GAd8FCbjlaxx7LwSebvuZbnmc/6LV5Rc="),
    )

  def test_hex_to_b64(self):
    self.assertEqual(
      "shlVQpOOGy+GAd8FCbjlaxx7LwSebvuZbnmc/6LV5Rc=",
      hex_to_b64("b2195542938e1b2f8601df0509b8e56b1c7b2f049e6efb996e799cffa2d5e517"),
    )
