from .transaction import Transaction
from ..outputs import crypto_transfer_pb2, transaction_body_pb2, basic_types_pb2
from ..account.account_id import AccountId
from ..tokens.token_id import TokenId
from collections import defaultdict

class TransferTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self.hbar_transfers = defaultdict(int)  
        self.token_transfers = defaultdict(lambda: defaultdict(int)) 

    def add_hbar_transfer(self, account_id, amount):
        account_id_str = str(account_id)
        self.hbar_transfers[account_id_str] += amount
        return self

    def add_token_transfer(self, token_id, account_id, amount):
        token_id_str = str(token_id)
        account_id_str = str(account_id)
        self.token_transfers[token_id_str][account_id_str] += amount
        return self

    def build_transaction_body(self):
        crypto_transfer_tx_body = crypto_transfer_pb2.CryptoTransferTransactionBody()
        
        # HBAR 
        if self.hbar_transfers:
            transfer_list = basic_types_pb2.TransferList()
            for account_id_str, amount in self.hbar_transfers.items():
                account_id = AccountId.from_string(account_id_str)
                account_amount = basic_types_pb2.AccountAmount()
                account_amount.accountID.CopyFrom(account_id.to_proto())
                account_amount.amount = amount  # Amount in tinybars
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
        
        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id)
        transaction_body.transactionFee = self.transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration_seconds
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo
        transaction_body.cryptoTransfer.CopyFrom(crypto_transfer_tx_body)

        return transaction_body
