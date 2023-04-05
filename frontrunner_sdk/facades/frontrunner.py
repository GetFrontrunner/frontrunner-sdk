from typing import Optional

from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsOperation # NOQA
from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsRequest # NOQA
from frontrunner_sdk.commands.frontrunner.list_markets import ListMarketsResponse # NOQA
from frontrunner_sdk.facades.base import FrontrunnerFacadeMixin # NOQA
from frontrunner_sdk.ioc import FrontrunnerIoC
from frontrunner_sdk.openapi.frontrunner_api.models.market_status import MarketStatus # NOQA
from frontrunner_sdk.sync import SyncMixin


class FrontrunnerFacadeAsync(FrontrunnerFacadeMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.deps = deps

  async def list_markets(
    self,
    id: Optional[str] = None,
    injective_id: Optional[str] = None,
    prop_id: Optional[str] = None,
    event_id: Optional[str] = None,
    league_id: Optional[str] = None,
    status: Optional[MarketStatus] = None,
  ) -> ListMarketsResponse:
    request = ListMarketsRequest(
      id=id,
      injective_id=injective_id,
      prop_id=prop_id,
      event_id=event_id,
      league_id=league_id,
      status=status,
    )

    return await self._run_operation(ListMarketsOperation, self.deps, request)


class FrontrunnerFacade(SyncMixin):

  def __init__(self, deps: FrontrunnerIoC):
    self.impl = FrontrunnerFacadeAsync(deps)

  def list_markets(
    self,
    id: Optional[str] = None,
    injective_id: Optional[str] = None,
    prop_id: Optional[str] = None,
    event_id: Optional[str] = None,
    league_id: Optional[str] = None,
    status: Optional[MarketStatus] = None,
  ) -> ListMarketsResponse:
    return self._synchronously(
      self.impl.list_markets,
      id=id,
      injective_id=injective_id,
      prop_id=prop_id,
      event_id=event_id,
      league_id=league_id,
      status=status,
    )
