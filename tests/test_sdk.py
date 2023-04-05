from unittest import TestCase

from frontrunner_sdk.facades.frontrunner import Frontrunner
from frontrunner_sdk.facades.frontrunner import FrontrunnerAsync
from frontrunner_sdk.facades.injective import Injective
from frontrunner_sdk.facades.injective import InjectiveAsync
from frontrunner_sdk.sdk import FrontrunnerSDK
from frontrunner_sdk.sdk import FrontrunnerSDKAsync


class TestFrontrunnerSDKAsync(TestCase):

  def test_has_operation_namespaces(self):
    sdk = FrontrunnerSDKAsync()

    self.assertIsInstance(sdk.frontrunner, FrontrunnerAsync)
    self.assertIsInstance(sdk.injective, InjectiveAsync)


class TestFrontrunnerSDK(TestCase):

  def test_has_operation_namespaces(self):
    sdk = FrontrunnerSDK()

    self.assertIsInstance(sdk.frontrunner, Frontrunner)
    self.assertIsInstance(sdk.injective, Injective)
