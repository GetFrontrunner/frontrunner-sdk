from unittest import TestCase

from frontrunner_sdk.exceptions import FrontrunnerException


class TestFrontrunnerException(TestCase):

  def test_str_message_only(self):
    exception = FrontrunnerException("Something went wrong")
    self.assertEqual(str(exception), "Something went wrong")

  def test_str_message_with_subjects(self):
    exception = FrontrunnerException(
      "Something went wrong",
      int=7,
      list=[0, 9],
      str="boom",
    )

    self.assertEqual(str(exception), "Something went wrong int=7 list=[0, 9] str='boom'")
