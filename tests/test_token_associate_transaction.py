import pytest
from unittest.mock import MagicMock
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.utils import generate_transaction_id

def test_build_transaction_body(mock_account_ids):
    """Test building the token associate transaction body with valid account ID and token IDs."""
    account_id, _, node_account_id, token_id_1, token_id_2 = mock_account_ids
    associate_tx = TokenAssociateTransaction()

    # set accountId and tokenId
    associate_tx.account_id = account_id
    associate_tx.token_ids = [token_id_1, token_id_2]
    associate_tx.transaction_id = generate_transaction_id(account_id.to_proto())
    associate_tx.node_account_id = node_account_id 

    transaction_body = associate_tx.build_transaction_body()

    # verify tx body fields
    assert transaction_body.tokenAssociate.account.shardNum == account_id.shard
    assert transaction_body.tokenAssociate.account.realmNum == account_id.realm
    assert transaction_body.tokenAssociate.account.accountNum == account_id.num
    assert len(transaction_body.tokenAssociate.tokens) == 2
    assert transaction_body.tokenAssociate.tokens[0].tokenNum == token_id_1.num
    assert transaction_body.tokenAssociate.tokens[1].tokenNum == token_id_2.num

def test_missing_fields():
    """Test that building the transaction without account ID or token IDs raises a ValueError."""
    associate_tx = TokenAssociateTransaction()

    # expect error when account ID and token IDs are not set
    with pytest.raises(ValueError, match="Account ID and token IDs must be set"):
        associate_tx.build_transaction_body()

def test_sign_transaction(mock_account_ids):
    """Test signing the token associate transaction with a private key."""
    account_id, _, node_account_id, token_id_1, _ = mock_account_ids
    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = account_id
    associate_tx.token_ids = [token_id_1]
    associate_tx.transaction_id = generate_transaction_id(account_id.to_proto())
    associate_tx.node_account_id = node_account_id 

    # mock private key and signing operation
    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    # sign transaction
    associate_tx.sign(private_key)

    # verify signature map contains a signature pair
    assert len(associate_tx.signature_map.sigPair) == 1
    sig_pair = associate_tx.signature_map.sigPair[0]

    assert sig_pair.pubKeyPrefix == b'public'
    assert sig_pair.ed25519 == b'signature'

def test_to_proto(mock_account_ids):
    """Test converting the token associate transaction to protobuf format after signing."""
    account_id, _, node_account_id, token_id_1, _ = mock_account_ids
    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = account_id
    associate_tx.token_ids = [token_id_1]
    associate_tx.transaction_id = generate_transaction_id(account_id.to_proto())
    associate_tx.node_account_id = node_account_id  

    # mock private key for signing
    private_key = MagicMock()
    private_key.sign.return_value = b'signature'
    private_key.public_key().public_bytes.return_value = b'public_key'

    # sign and convert to protobuf
    associate_tx.sign(private_key)
    proto = associate_tx.to_proto()

    # verify protobuf contains signed bytes
    assert proto.signedTransactionBytes
    assert len(proto.signedTransactionBytes) > 0
