from src.outputs import basic_types_pb2, timestamp_pb2, transaction_pb2, transaction_contents_pb2, response_code_pb2
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

def generate_transaction_id(account_id_proto):
    """
    Generate a unique transaction ID based on the account ID and the current timestamp.
    """
    import time
    from random import randint

    timestamp = int(time.time())
    nanos = randint(0, 999999999)

    tx_timestamp = timestamp_pb2.Timestamp(seconds=timestamp, nanos=nanos)

    tx_id = basic_types_pb2.TransactionID(
        transactionValidStart=tx_timestamp,
        accountID=account_id_proto
    )
    return tx_id

def sign_transaction(transaction, private_key):
    # sign the transaction using the operator's private key
    transaction_body = transaction.build_transaction_body()
    transaction_body_bytes = transaction_body.SerializeToString()

    signature = private_key.sign(transaction_body_bytes)

    public_key_bytes = private_key.public_key().public_bytes(
        encoding=Encoding.Raw,
        format=PublicFormat.Raw
    )

    sig_pair = basic_types_pb2.SignaturePair(
        pubKeyPrefix=public_key_bytes[:6],
        ed25519=signature
    )

    sig_map = basic_types_pb2.SignatureMap(sigPair=[sig_pair])

    signed_transaction = transaction_contents_pb2.SignedTransaction(
        bodyBytes=transaction_body_bytes,
        sigMap=sig_map
    )

    transaction._signed_transaction_bytes = signed_transaction.SerializeToString()

def serialize_transaction(transaction):
    # serialize the signed transaction into a protobuf message
    if transaction._signed_transaction_bytes is None:
        raise Exception("Transaction must be signed before calling to_proto()")
    return transaction_pb2.Transaction(
        signedTransactionBytes=transaction._signed_transaction_bytes
    )