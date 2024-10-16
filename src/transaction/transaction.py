from src.outputs import transaction_pb2, transaction_body_pb2, basic_types_pb2, transaction_contents_pb2
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
        if self.transaction_body_bytes is None:
            transaction_body = self.build_transaction_body()
            self.transaction_body_bytes = transaction_body.SerializeToString()

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
        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be signed before calling to_proto()")

        signed_transaction = transaction_contents_pb2.SignedTransaction(
            bodyBytes=self.transaction_body_bytes,
            sigMap=self.signature_map
        )

        transaction = transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )
        return transaction

    def build_transaction_body(self):
        raise NotImplementedError("Must implement build_transaction_body in subclass")
