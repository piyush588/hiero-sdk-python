from src.outputs import transaction_pb2, transaction_body_pb2, basic_types_pb2, transaction_contents_pb2, token_create_pb2, token_associate_pb2, crypto_transfer_pb2
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

class Transaction:
    def __init__(self):
        self.transaction_id = None
        self.node_account_id = None
        self.transaction_fee = 100_000_000
        self.transaction_valid_duration_seconds = 120
        self.generate_record = False
        self.memo = ""
        self.transaction_body_bytes = None
        self.signature_map = basic_types_pb2.SignatureMap()

    def sign(self, private_key):
        """
        Sign the transaction using the provided private key.
        """
        if self.transaction_body_bytes is None:
            self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        signature = private_key.sign(self.transaction_body_bytes)

        public_key_bytes = private_key.public_key().public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )

        sig_pair = basic_types_pb2.SignaturePair(
            pubKeyPrefix=public_key_bytes[:6],
            ed25519=signature
        )

        self.signature_map.sigPair.append(sig_pair)

    def to_proto(self):
        """
        Serialize the signed transaction into a protobuf message.
        """
        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be signed before calling to_proto()")

        signed_transaction = transaction_contents_pb2.SignedTransaction(
            bodyBytes=self.transaction_body_bytes,
            sigMap=self.signature_map
        )

        return transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )

    def setup_base_transaction(self, transaction_id, node_account_id, transaction_fee=None, memo=None):
        """
        Common function to set up the base transaction fields. This can be reused by different transaction types.
        """
        self.transaction_id = transaction_id
        self.node_account_id = node_account_id
        if transaction_fee is not None:
            self.transaction_fee = transaction_fee
        if memo is not None:
            self.memo = memo

    def build_base_transaction_body(self, specific_tx_body):
        """
        Builds the base transaction body by combining the base transaction fields 
        with the specific transaction body fields (e.g., token associate, transfer).
        """
        transaction_body = transaction_body_pb2.TransactionBody()
        
        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id)
        transaction_body.transactionFee = self.transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration_seconds
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        # set specific transaction body (like token associate, transfer, etc.)
        if isinstance(specific_tx_body, token_create_pb2.TokenCreateTransactionBody):
            transaction_body.tokenCreation.CopyFrom(specific_tx_body)
        elif isinstance(specific_tx_body, token_associate_pb2.TokenAssociateTransactionBody):
            transaction_body.tokenAssociate.CopyFrom(specific_tx_body)
        elif isinstance(specific_tx_body, crypto_transfer_pb2.CryptoTransferTransactionBody):
            transaction_body.cryptoTransfer.CopyFrom(specific_tx_body)
        # add more here if extending SDK
        else:
            raise ValueError("Unsupported transaction type")

        return transaction_body
