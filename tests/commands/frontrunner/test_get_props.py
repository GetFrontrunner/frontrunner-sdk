from typing import List
from typing import Optional
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from frontrunner_sdk.commands.frontrunner.get_props import GetPropsRequest, GetPropsOperation
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api import Prop


class TestGetPropsOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)

  def setup_partner_api(
    self,
    props: Optional[List[Prop]] = None,
  ):
    self.deps.openapi_frontrunner_api.get_props = AsyncMock(return_value=props or [])

  async def test_get_props(self):
    props = [Prop(id="prop", name="prop-name")]
    self.setup_partner_api(props=props,)

    req = GetPropsRequest(id="prop",)

    cmd = GetPropsOperation(req)
    res = await cmd.execute(self.deps)

    self.assertEqual(res.props, props)
