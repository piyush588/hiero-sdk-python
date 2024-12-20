import pytest
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.tokens.token_id import TokenId

@pytest.fixture
def mock_account_ids():
    """Fixture to provide mock account IDs and token IDs."""
    account_id_sender = AccountId(0, 0, 1)
    account_id_recipient = AccountId(0, 0, 2)
    node_account_id = AccountId(0, 0, 3)
    token_id_1 = TokenId(1, 1, 1)
    token_id_2 = TokenId(2, 2, 2)
    return account_id_sender, account_id_recipient, node_account_id, token_id_1, token_id_2
