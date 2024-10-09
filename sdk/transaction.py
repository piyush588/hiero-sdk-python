# sdk/transaction.py
from sdk.outputs import transaction_pb2
from sdk.crypto.private_key import PrivateKey
from sdk.crypto.public_key import PublicKey

class Transaction:
    def __init__(self):
        self.transaction_id = None  
        self.node_account_id = None  
        self.signed_transaction = None

    def sign(self, private_key: PrivateKey):
        transaction_body = self.build_transaction_body()
        serialized_body = transaction_body.SerializeToString()
        signature = private_key.sign(serialized_body)

        sig_pair = transaction_pb2.SignaturePair(
            pubKeyPrefix=private_key.public_key().to_bytes()[:6],
            ed25519=signature
        )

        sig_map = transaction_pb2.SignatureMap(sigPair=[sig_pair])

        self.signed_transaction = transaction_pb2.SignedTransaction(
            bodyBytes=serialized_body,
            sigMap=sig_map
        )

    def to_proto(self):
        return transaction_pb2.Transaction(
            signedTransactionBytes=self.signed_transaction.SerializeToString()
        )

    def build_transaction_body(self):
        raise NotImplementedError("Must implement build_transaction_body in subclass")