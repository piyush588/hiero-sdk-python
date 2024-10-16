import unittest
from unittest.mock import MagicMock
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from src.utils import generate_transaction_id

class TestTokenAssociateTransaction(unittest.TestCase):
    """
    Unit tests for the TokenAssociateTransaction class.
    """

    def setUp(self):
        """
        Set up the test environment with mock values for account ID and token IDs.
        """
        self.account_id = AccountId(0, 0, 1001)
        self.token_id_1 = TokenId(1, 1, 1)
        self.token_id_2 = TokenId(2, 2, 2)
        self.node_account_id = AccountId(0, 0, 3)

    def test_build_transaction_body(self):
        """
        Test building the token associate transaction body with valid account ID and token IDs.
        """
        associate_tx = TokenAssociateTransaction()

        # set accountId and tokenId
        associate_tx.account_id = self.account_id
        associate_tx.token_ids = [self.token_id_1, self.token_id_2]
        associate_tx.transaction_id = generate_transaction_id(self.account_id.to_proto())
        associate_tx.node_account_id = self.node_account_id.to_proto()

        transaction_body = associate_tx.build_transaction_body()

        # verify tx body fields
        self.assertEqual(transaction_body.tokenAssociate.account.shardNum, self.account_id.shard)
        self.assertEqual(transaction_body.tokenAssociate.account.realmNum, self.account_id.realm)
        self.assertEqual(transaction_body.tokenAssociate.account.accountNum, self.account_id.num)
        self.assertEqual(len(transaction_body.tokenAssociate.tokens), 2)
        self.assertEqual(transaction_body.tokenAssociate.tokens[0].tokenNum, self.token_id_1.num)
        self.assertEqual(transaction_body.tokenAssociate.tokens[1].tokenNum, self.token_id_2.num)

    def test_missing_fields(self):
        """
        Test that building the transaction without account ID or token IDs raises a ValueError.
        """
        associate_tx = TokenAssociateTransaction()

        # expect error when account ID and token IDs are not set
        with self.assertRaises(ValueError) as context:
            associate_tx.build_transaction_body()

        self.assertTrue("Account ID and token IDs must be set" in str(context.exception))

    def test_sign_transaction(self):
        """
        Test signing the token associate transaction with a private key.
        """
        associate_tx = TokenAssociateTransaction()
        associate_tx.account_id = self.account_id
        associate_tx.token_ids = [self.token_id_1]
        associate_tx.transaction_id = generate_transaction_id(self.account_id.to_proto())
        associate_tx.node_account_id = self.node_account_id.to_proto()

        # mock private key and signing operation
        private_key = MagicMock()
        private_key.sign.return_value = b'signature'
        private_key.public_key().public_bytes.return_value = b'public_key'

        # sign transaction
        associate_tx.sign(private_key)

        # verify signature map contains a signature pair
        self.assertEqual(len(associate_tx.signature_map.sigPair), 1)
        sig_pair = associate_tx.signature_map.sigPair[0]

        self.assertEqual(sig_pair.pubKeyPrefix, b'public')  
        self.assertEqual(sig_pair.ed25519, b'signature')

    def test_to_proto(self):
        """
        Test converting the token associate transaction to protobuf format after signing.
        """
        associate_tx = TokenAssociateTransaction()
        associate_tx.account_id = self.account_id
        associate_tx.token_ids = [self.token_id_1]
        associate_tx.transaction_id = generate_transaction_id(self.account_id.to_proto())
        associate_tx.node_account_id = self.node_account_id.to_proto()

        # mock private key for signing
        private_key = MagicMock()
        private_key.sign.return_value = b'signature'
        private_key.public_key().public_bytes.return_value = b'public_key'

        # sign and convert to protobuf
        associate_tx.sign(private_key)
        proto = associate_tx.to_proto()

        # verify protobuf contains signed bytes
        self.assertTrue(proto.signedTransactionBytes)
        self.assertGreater(len(proto.signedTransactionBytes), 0)

if __name__ == "__main__":
    unittest.main()
