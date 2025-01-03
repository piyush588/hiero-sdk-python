import pytest
from unittest.mock import MagicMock
from hedera_sdk_python.query.account_balance_query import CryptoGetAccountBalanceQuery
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.account.account_balance import AccountBalance
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.hbar import Hbar
from hedera_sdk_python.response_code import ResponseCode

@pytest.mark.usefixtures("mock_account_ids")
def test_build_account_balance_query(mock_account_ids):
    """
    Test building a CryptoGetAccountBalanceQuery with a valid account ID.
    """
    account_id_sender, account_id_recipient, node_account_id, token_id_1, token_id_2 = mock_account_ids
    query = CryptoGetAccountBalanceQuery(account_id=account_id_sender)
    assert query.account_id == account_id_sender

@pytest.mark.usefixtures("mock_account_ids")
def test_execute_account_balance_query(mock_account_ids):
    """
    Test executing the CryptoGetAccountBalanceQuery with a mocked client.
    """
    account_id_sender, account_id_recipient, node_account_id, token_id_1, token_id_2 = mock_account_ids
    query = CryptoGetAccountBalanceQuery().set_account_id(account_id_sender)
    mock_client = MagicMock(spec=Client)
    mock_response = MagicMock()
    mock_response.cryptogetAccountBalance.balance = 100000000
    mock_response.cryptogetAccountBalance.tokenBalances = []
    mock_response.cryptogetAccountBalance.header.nodeTransactionPrecheckCode = ResponseCode.OK
    mock_client.send_query = MagicMock(return_value=mock_response)
    query.node_account_ids = [node_account_id]
    query._make_request = MagicMock(return_value="fake_request")
    query._get_status_from_response = MagicMock(return_value=ResponseCode.OK)
    query._map_response = MagicMock(
        return_value=AccountBalance(Hbar.from_tinybars(100000000))
    )
    balance = query.execute(mock_client)
    assert balance.hbars.to_tinybars() == 100000000
    print("Test passed: CryptoGetAccountBalanceQuery executed successfully.")
