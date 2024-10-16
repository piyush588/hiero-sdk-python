import unittest
from src.transaction.transfer_transaction import TransferTransaction
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from src.outputs import basic_types_pb2
from src.utils import generate_transaction_id

class TestTransferTransaction(unittest.TestCase):

    def setUp(self):
        """Set up initial values for account and token IDs used in tests."""
        self.token_id = TokenId(1, 1, 1)
        self.account_id_sender = AccountId(0, 0, 1)
        self.account_id_recipient = AccountId(0, 0, 2)
        self.node_account_id = AccountId(0, 0, 3)

    def test_add_token_transfer(self):
        """Test adding token transfers and ensure amounts are correctly added."""
        transfer_tx = TransferTransaction()

        transfer_tx.add_token_transfer(self.token_id, self.account_id_sender, -100)
        transfer_tx.add_token_transfer(self.token_id, self.account_id_recipient, 100)

        # verify amounts were added correctly
        token_transfers = transfer_tx.token_transfers[str(self.token_id)]
        self.assertEqual(token_transfers[str(self.account_id_sender)], -100)
        self.assertEqual(token_transfers[str(self.account_id_recipient)], 100)

    def test_add_hbar_transfer(self):
        """Test adding HBAR transfers and ensure amounts are correctly added."""
        transfer_tx = TransferTransaction()

        transfer_tx.add_hbar_transfer(self.account_id_sender, -500)
        transfer_tx.add_hbar_transfer(self.account_id_recipient, 500)

        self.assertEqual(transfer_tx.hbar_transfers[str(self.account_id_sender)], -500)
        self.assertEqual(transfer_tx.hbar_transfers[str(self.account_id_recipient)], 500)

    def test_add_invalid_transfer(self):
        """Test adding invalid transfers raises the appropriate error."""
        transfer_tx = TransferTransaction()

        with self.assertRaises(TypeError):
            transfer_tx.add_hbar_transfer(12345, -500)  # invalid account_id type

        with self.assertRaises(ValueError):
            transfer_tx.add_hbar_transfer(self.account_id_sender, 0)  # invalid amount (zero)

        with self.assertRaises(TypeError):
            transfer_tx.add_token_transfer(12345, self.account_id_sender, -100)  # Invalid token_id type

    def test_empty_transfers(self):
        """Test that building a transaction with no transfers raises an error."""
        transfer_tx = TransferTransaction()
        
        transfer_tx.transaction_id = generate_transaction_id(self.account_id_sender.to_proto())
        transfer_tx.node_account_id = self.node_account_id.to_proto()

        transaction_body = transfer_tx.build_transaction_body()

        self.assertEqual(len(transaction_body.cryptoTransfer.transfers.accountAmounts), 0)
        self.assertEqual(len(transaction_body.cryptoTransfer.tokenTransfers), 0)

    def test_build_transaction_body(self):
        """Test building the transaction body with valid transfers."""
        transfer_tx = TransferTransaction()
        transfer_tx.add_token_transfer(self.token_id, self.account_id_sender, -100)
        transfer_tx.add_token_transfer(self.token_id, self.account_id_recipient, 100)

        # mock transactionId and node accountId
        transfer_tx.transaction_id = generate_transaction_id(self.account_id_sender.to_proto())
        transfer_tx.node_account_id = self.node_account_id.to_proto()

        transaction_body = transfer_tx.build_transaction_body()
        token_transfer_list = transaction_body.cryptoTransfer.tokenTransfers[0]

        self.assertEqual(token_transfer_list.token.shardNum, self.token_id.shard)
        self.assertEqual(token_transfer_list.token.realmNum, self.token_id.realm)
        self.assertEqual(token_transfer_list.token.tokenNum, self.token_id.num)

        sender_transfer = next(
            transfer for transfer in token_transfer_list.transfers
            if transfer.accountID == self.account_id_sender.to_proto()
        )
        recipient_transfer = next(
            transfer for transfer in token_transfer_list.transfers
            if transfer.accountID == self.account_id_recipient.to_proto()
        )

        self.assertEqual(sender_transfer.amount, -100)
        self.assertEqual(recipient_transfer.amount, 100)

if __name__ == "__main__":
    unittest.main()

