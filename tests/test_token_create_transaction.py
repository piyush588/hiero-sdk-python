import unittest
from unittest.mock import MagicMock
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.account.account_id import AccountId
from src.utils import generate_transaction_id
from cryptography.hazmat.primitives.asymmetric import ec

class TestTokenCreateTransaction(unittest.TestCase):
    """
    Unit tests for the TokenCreateTransaction class.
    """

    def setUp(self):
        """
        Set up initial values for token creation and account IDs used in tests.
        """
        self.token_name = "MyToken"
        self.token_symbol = "MTK"
        self.decimals = 2
        self.initial_supply = 1000
        self.treasury_account = AccountId(0, 0, 1001)
        self.node_account_id = AccountId(0, 0, 3)

    def test_build_transaction_body(self):
        """
        Test building a token creation transaction body with valid values.
        """
        token_tx = TokenCreateTransaction()

        token_tx.token_name = self.token_name
        token_tx.token_symbol = self.token_symbol
        token_tx.decimals = self.decimals
        token_tx.initial_supply = self.initial_supply
        token_tx.treasury_account_id = self.treasury_account
        token_tx.transaction_id = generate_transaction_id(self.treasury_account.to_proto())
        token_tx.node_account_id = self.node_account_id.to_proto()

        transaction_body = token_tx.build_transaction_body()

        # verify tx body fields
        self.assertEqual(transaction_body.tokenCreation.name, self.token_name)
        self.assertEqual(transaction_body.tokenCreation.symbol, self.token_symbol)
        self.assertEqual(transaction_body.tokenCreation.decimals, self.decimals)
        self.assertEqual(transaction_body.tokenCreation.initialSupply, self.initial_supply)

        # verify the treasury account values in protobuf
        treasury_account_proto = transaction_body.tokenCreation.treasury
        self.assertEqual(treasury_account_proto.shardNum, self.treasury_account.shard)
        self.assertEqual(treasury_account_proto.realmNum, self.treasury_account.realm)
        self.assertEqual(treasury_account_proto.accountNum, self.treasury_account.num)

    def test_missing_fields(self):
        """
        Test that building a transaction without required fields raises a ValueError.
        """
        token_tx = TokenCreateTransaction()
        with self.assertRaises(ValueError) as context:
            token_tx.build_transaction_body()

        self.assertTrue("Token name, symbol, and treasury account ID must be set" in str(context.exception))

    def test_sign_transaction(self):
        """
        Test signing the token creation transaction with a private key.
        """
        token_tx = TokenCreateTransaction()
        token_tx.token_name = self.token_name
        token_tx.token_symbol = self.token_symbol
        token_tx.treasury_account_id = self.treasury_account
        token_tx.transaction_id = generate_transaction_id(self.treasury_account.to_proto())
        token_tx.node_account_id = self.node_account_id.to_proto()

        private_key = MagicMock()
        private_key.sign.return_value = b'signature'
        private_key.public_key().public_bytes.return_value = b'public_key'

        # sign transaction
        token_tx.sign(private_key)

        # verify signature map
        self.assertEqual(len(token_tx.signature_map.sigPair), 1)
        sig_pair = token_tx.signature_map.sigPair[0]
        
        self.assertEqual(sig_pair.pubKeyPrefix, b'public')  
        self.assertEqual(sig_pair.ed25519, b'signature')

    def test_to_proto(self):
        """
        Test converting the token creation transaction to protobuf format after signing.
        """
        token_tx = TokenCreateTransaction()
        token_tx.token_name = self.token_name
        token_tx.token_symbol = self.token_symbol
        token_tx.treasury_account_id = self.treasury_account
        token_tx.transaction_id = generate_transaction_id(self.treasury_account.to_proto())
        token_tx.node_account_id = self.node_account_id.to_proto()

        private_key = MagicMock()
        private_key.sign.return_value = b'signature'
        private_key.public_key().public_bytes.return_value = b'public_key'

        # sign and convert to protobuf
        token_tx.sign(private_key)
        proto = token_tx.to_proto()

        # verify protobuf contains signed bytes
        self.assertTrue(proto.signedTransactionBytes)
        self.assertGreater(len(proto.signedTransactionBytes), 0)

    def test_set_transaction_fee(self):
        """
        Test setting the transaction fee for the token creation transaction.
        """
        token_tx = TokenCreateTransaction()
        token_tx.transaction_fee = 10_000_000  
        token_tx.token_name = self.token_name
        token_tx.token_symbol = self.token_symbol
        token_tx.treasury_account_id = self.treasury_account
        token_tx.transaction_id = generate_transaction_id(self.treasury_account.to_proto())
        token_tx.node_account_id = self.node_account_id.to_proto()

        transaction_body = token_tx.build_transaction_body()
        self.assertEqual(transaction_body.transactionFee, 10_000_000)

if __name__ == "__main__":
    unittest.main()
