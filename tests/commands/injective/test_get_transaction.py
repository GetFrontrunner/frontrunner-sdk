import json

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import Mock

from frontrunner_sdk import FrontrunnerIoC
from frontrunner_sdk.commands.injective.get_transaction import GetTransactionOperation # NOQA
from frontrunner_sdk.commands.injective.get_transaction import GetTransactionRequest # NOQA
from frontrunner_sdk.commands.injective.get_transaction import OrderFailure
from frontrunner_sdk.helpers.encoders import b64_to_hex


class TestGetTransactionOperation(IsolatedAsyncioTestCase):

  def setUp(self) -> None:
    self.deps = MagicMock(spec=FrontrunnerIoC)
    self.flags = [59]
    self.b64_hashes = ["3LVlH0iM5ZvkrZd9yCOZP5F3bgSEjPm7oPEkkOl7ank="]
    self.hashes = ["0x" + b64_to_hex(h) for h in self.b64_hashes]

  def test_validate(self):
    req = GetTransactionRequest(transaction_hash="abc")
    cmd = GetTransactionOperation(req)
    cmd.validate(self.deps)

  async def test_get_transaction_order_failures(self):
    mock_attributes = [
      Mock(key="flags", value=json.dumps(self.flags)),
      Mock(key="hashes", value=json.dumps(self.b64_hashes))
    ]
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
    mock_tx_response.logs = None
    mock_response.tx_response = mock_tx_response
    self.deps.injective_client.get_tx = AsyncMock(return_value=mock_response)

    result = await GetTransactionOperation(GetTransactionRequest(transaction_hash="abc")).execute(self.deps)

    self.assertEqual(mock_response, result.injective_response)
    self.assertEqual([], result.order_failures)
