from .transaction import Transaction
from ..outputs import crypto_transfer_pb2, basic_types_pb2
from ..account.account_id import AccountId
from ..tokens.token_id import TokenId
from collections import defaultdict

class TransferTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self.hbar_transfers = defaultdict(int)
        self.token_transfers = defaultdict(lambda: defaultdict(int))

    def add_hbar_transfer(self, account_id, amount):
        """
        Add a HBAR transfer to the transaction.
        """
        if not isinstance(account_id, (AccountId, str)):
            raise TypeError("account_id must be an AccountId or string")
        if not isinstance(amount, int) or amount == 0:
            raise ValueError("Amount must be a non-zero integer")

        account_id_str = str(account_id)
        self.hbar_transfers[account_id_str] += amount
        return self

    def add_token_transfer(self, token_id, account_id, amount):
        """
        Add a token transfer to the transaction.
        """
        if not isinstance(token_id, (TokenId, str)):
            raise TypeError("token_id must be a TokenId or string")
        if not isinstance(account_id, (AccountId, str)):
            raise TypeError("account_id must be an AccountId or string")
        if not isinstance(amount, int) or amount == 0:
            raise ValueError("Amount must be a non-zero integer")

        token_id_str = str(token_id)
        account_id_str = str(account_id)
        self.token_transfers[token_id_str][account_id_str] += amount
        return self

    def build_transaction_body(self):
        """
        Build and return the protobuf transaction body for a transfer transaction.
        """
        crypto_transfer_tx_body = crypto_transfer_pb2.CryptoTransferTransactionBody()

        # HBAR
        if self.hbar_transfers:
            transfer_list = basic_types_pb2.TransferList()
            for account_id_str, amount in self.hbar_transfers.items():
                account_id = AccountId.from_string(account_id_str)
                account_amount = basic_types_pb2.AccountAmount()
                account_amount.accountID.CopyFrom(account_id.to_proto())
                account_amount.amount = amount
                transfer_list.accountAmounts.append(account_amount)
            crypto_transfer_tx_body.transfers.CopyFrom(transfer_list)

        # Token
        for token_id_str, transfers in self.token_transfers.items():
            token_id = TokenId.from_string(token_id_str)
            token_transfer_list = basic_types_pb2.TokenTransferList()
            token_transfer_list.token.CopyFrom(token_id.to_proto())
            for account_id_str, amount in transfers.items():
                account_id = AccountId.from_string(account_id_str)
                account_amount = basic_types_pb2.AccountAmount()
                account_amount.accountID.CopyFrom(account_id.to_proto())
                account_amount.amount = amount
                token_transfer_list.transfers.append(account_amount)
            crypto_transfer_tx_body.tokenTransfers.append(token_transfer_list)

        return self.build_base_transaction_body(crypto_transfer_tx_body)