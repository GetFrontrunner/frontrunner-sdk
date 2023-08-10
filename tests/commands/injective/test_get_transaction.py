import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, Mock

from frontrunner_sdk import FrontrunnerIoC
from frontrunner_sdk.commands.injective.get_transaction import GetTransactionOperation, OrderFailure  # NOQA
from frontrunner_sdk.commands.injective.get_transaction import GetTransactionRequest  # NOQA
from frontrunner_sdk.exceptions import FrontrunnerArgumentException  # NOQA


class TestGetTransactionOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.flags = [59]
    self.hashes = ["3LVlH0iM5ZvkrZd9yCOZP5F3bgSEjPm7oPEkkOl7ank="]

  def test_validate(self):
    req = GetTransactionRequest(transaction_hash="abc")
    cmd = GetTransactionOperation(req)
    cmd.validate(self.deps)

  async def test_get_transaction_order_failures(self):
    mock_attributes = [Mock(key="flags", value=json.dumps(self.flags)), Mock(key="hashes", value=json.dumps(self.hashes))]
    mock_log = Mock(events=[Mock(type="injective.exchange.v1beta1.EventOrderFail", attributes=mock_attributes)])
    mock_response = mock_tx_response = Mock()
    mock_tx_response.logs = [mock_log]
    mock_response.tx_response = mock_tx_response
    self.deps.injective_client.get_tx = AsyncMock(return_value=mock_response)

    result = await GetTransactionOperation(GetTransactionRequest(transaction_hash="abc")).execute(self.deps)

    self.assertEqual(mock_response, result.injective_response)
    self.assertEqual([OrderFailure(self.flags, self.hashes)], result.order_failures)

  async def test_get_transaction_no_order_failures(self):
    mock_response = mock_tx_response = Mock()
    mock_response.tx_response = mock_tx_response
    self.deps.injective_client.get_tx = AsyncMock(return_value=mock_response)

    result = await GetTransactionOperation(GetTransactionRequest(transaction_hash="abc")).execute(self.deps)

    self.assertEqual(mock_response, result.injective_response)
    self.assertEqual([], result.order_failures)
