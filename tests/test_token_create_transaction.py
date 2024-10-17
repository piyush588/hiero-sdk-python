import pytest
from unittest.mock import MagicMock
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.utils import generate_transaction_id

def test_build_transaction_body(mock_account_ids):
    """Test building a token creation transaction body with valid values."""
    _, _, node_account_id, _, _ = mock_account_ids
    token_name = "MyToken"
    token_symbol = "MTK"
    decimals = 2
    initial_supply = 1000
    treasury_account = mock_account_ids[0]

    token_tx = TokenCreateTransaction()

    token_tx.token_name = token_name
    token_tx.token_symbol = token_symbol
    token_tx.decimals = decimals
    token_tx.initial_supply = initial_supply
    token_tx.treasury_account_id = treasury_account
    token_tx.transaction_id = generate_transaction_id(treasury_account.to_proto())
    token_tx.node_account_id = node_account_id  

    transaction_body = token_tx.build_transaction_body()

    # verify tx body fields
    assert transaction_body.tokenCreation.name == token_name
    assert transaction_body.tokenCreation.symbol == token_symbol
    assert transaction_body.tokenCreation.decimals == decimals
    assert transaction_body.tokenCreation.initialSupply == initial_supply

def test_missing_fields():
    """Test that building a transaction without required fields raises a ValueError."""
    token_tx = TokenCreateTransaction()
    with pytest.raises(ValueError, match="Token name, symbol, and treasury account ID must be set"):
        token_tx.build_transaction_body()

def test_sign_transaction(mock_account_ids):
    """Test signing the token creation transaction with a private key."""
    account_id_sender, _, node_account_id, _, _ = mock_account_ids
    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.treasury_account_id = account_id_sender
    token_tx.transaction_id = generate_transaction_id(account_id_sender.to_proto())
    token_tx.node_account_id = node_account_id  

    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    # sign transaction
    token_tx.sign(private_key)

    # verify signature map
    assert len(token_tx.signature_map.sigPair) == 1
    sig_pair = token_tx.signature_map.sigPair[0]
    assert sig_pair.pubKeyPrefix == b'public'
    assert sig_pair.ed25519 == b'signature'

def test_to_proto(mock_account_ids):
    """Test converting the token creation transaction to protobuf format after signing."""
    account_id_sender, _, node_account_id, _, _ = mock_account_ids
    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.treasury_account_id = account_id_sender
    token_tx.transaction_id = generate_transaction_id(account_id_sender.to_proto())
    token_tx.node_account_id = node_account_id 

    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    # sign and convert to protobuf
    token_tx.sign(private_key)
    proto = token_tx.to_proto()

    # verify protobuf contains signed bytes
    assert proto.signedTransactionBytes
    assert len(proto.signedTransactionBytes) > 0
