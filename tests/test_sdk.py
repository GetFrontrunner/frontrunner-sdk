from unittest import TestCase

from frontrunner_sdk.facades.frontrunner import FrontrunnerFacade
from frontrunner_sdk.facades.frontrunner import FrontrunnerFacadeAsync
from frontrunner_sdk.facades.injective import InjectiveFacade
from frontrunner_sdk.facades.injective import InjectiveFacadeAsync
from frontrunner_sdk.sdk import FrontrunnerSDK
from frontrunner_sdk.sdk import FrontrunnerSDKAsync


class TestFrontrunnerSDKAsync(TestCase):

  def test_has_operation_namespaces(self):
    sdk = FrontrunnerSDKAsync()

    self.assertIsInstance(sdk.frontrunner, FrontrunnerFacadeAsync)
    self.assertIsInstance(sdk.injective, InjectiveFacadeAsync)


class TestFrontrunnerSDK(TestCase):

  def test_has_operation_namespaces(self):
    sdk = FrontrunnerSDK()

    self.assertIsInstance(sdk.frontrunner, FrontrunnerFacade)
    self.assertIsInstance(sdk.injective, InjectiveFacade)
