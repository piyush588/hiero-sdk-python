from src.transaction.transaction import Transaction
from src.outputs import token_create_pb2, transaction_body_pb2
from src.outputs import basic_types_pb2

class TokenCreateTransaction(Transaction):
    def __init__(self):
        super().__init__()
        self.token_name = None
        self.token_symbol = None
        self.decimals = 0
        self.initial_supply = 0
        self.treasury_account_id = None  

    def build_transaction_body(self):
        if not all([self.token_name, self.token_symbol, self.treasury_account_id]):
            raise ValueError("Token name, symbol, and treasury account ID must be set")

        # initialize txbody
        token_create_tx_body = token_create_pb2.TokenCreateTransactionBody()
        token_create_tx_body.name = self.token_name
        token_create_tx_body.symbol = self.token_symbol
        token_create_tx_body.decimals = self.decimals
        token_create_tx_body.initialSupply = self.initial_supply

        token_create_tx_body.treasury.CopyFrom(self.treasury_account_id.to_proto())

        # build txbody
        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id)
        transaction_body.transactionFee = self.transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration_seconds
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        transaction_body.tokenCreation.CopyFrom(token_create_tx_body)

        return transaction_body
