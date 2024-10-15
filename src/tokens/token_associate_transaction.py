from src.transaction.transaction import Transaction
from src.outputs import token_associate_pb2, transaction_body_pb2

class TokenAssociateTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self.account_id = None
        self.token_ids = []

    def build_transaction_body(self):
        if not self.account_id or not self.token_ids:
            raise ValueError("Account ID and token IDs must be set")

        token_associate_tx_body = token_associate_pb2.TokenAssociateTransactionBody()
        token_associate_tx_body.account.CopyFrom(self.account_id.to_proto())
        token_associate_tx_body.tokens.extend([token_id.to_proto() for token_id in self.token_ids])

        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id)
        transaction_body.transactionFee = self.transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration_seconds
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        transaction_body.tokenAssociate.CopyFrom(token_associate_tx_body)

        return transaction_body
