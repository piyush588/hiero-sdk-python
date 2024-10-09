from sdk.outputs import transaction_contents_pb2
from sdk.outputs import transaction_pb2
from sdk.outputs import transaction_body_pb2
from sdk.outputs import token_create_pb2
from sdk.outputs import basic_types_pb2
from cryptography.hazmat.primitives import serialization


class TokenCreateTransaction:
    def __init__(self):
        self.transaction_id = None  
        self.node_account_id = None 
        self.token_name = None
        self.token_symbol = None
        self.decimals = None
        self.initial_supply = None
        self.treasury_account_id = None  
        self.transaction_fee = 100000000  
        self.transaction_valid_duration_seconds = 120  
        self.memo = ""
        self.generate_record = False

        self._signed_transaction_bytes = None  

    def sign(self, private_key):
        # Build the transaction body
        transaction_body = self._build_transaction_body()

        # Serialize the transaction body
        transaction_body_bytes = transaction_body.SerializeToString()

        # Sign the serialized transaction body
        signature = private_key.sign(transaction_body_bytes)

        # Create SignatureMap
        sig_map = basic_types_pb2.SignatureMap()
        sig_pair = basic_types_pb2.SignaturePair()

        # Get public key bytes
        public_key_bytes = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

        # Use a prefix of the public key
        sig_pair.pubKeyPrefix = public_key_bytes[:6]
        sig_pair.ed25519 = signature
        sig_map.sigPair.extend([sig_pair])

        # Construct the SignedTransaction
        signed_transaction = transaction_contents_pb2.SignedTransaction()
        signed_transaction.bodyBytes = transaction_body_bytes
        signed_transaction.sigMap.CopyFrom(sig_map)

        # Serialize the SignedTransaction
        self._signed_transaction_bytes = signed_transaction.SerializeToString()



    def to_proto(self):
        # Ensure that the transaction has been signed
        if self._signed_transaction_bytes is None:
            raise Exception("Transaction must be signed before calling to_proto()")

        # Construct the Transaction
        transaction = transaction_pb2.Transaction()
        transaction.signedTransactionBytes = self._signed_transaction_bytes

        return transaction


    def _build_transaction_body(self):
        # Construct the TokenCreateTransactionBody
        token_create_tx_body = token_create_pb2.TokenCreateTransactionBody()
        token_create_tx_body.name = self.token_name
        token_create_tx_body.symbol = self.token_symbol
        token_create_tx_body.decimals = self.decimals
        token_create_tx_body.initialSupply = self.initial_supply
        token_create_tx_body.treasury.CopyFrom(self.treasury_account_id.to_proto())

        # Construct the TransactionBody
        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id)
        transaction_body.transactionFee = self.transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration_seconds
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        # Set the token creation data
        transaction_body.tokenCreation.CopyFrom(token_create_tx_body)

        return transaction_body
