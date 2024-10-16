from src.transaction.transaction import Transaction
from src.outputs import token_associate_pb2

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

        return self.build_base_transaction_body(token_associate_tx_body)

    def set_common_fields(self, transaction_id, node_account_id, transaction_fee=None, memo=None):
        """ Use the setup_base_transaction method to set common fields. """
        self.setup_base_transaction(transaction_id, node_account_id, transaction_fee, memo)
