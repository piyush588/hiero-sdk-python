import time
from src.outputs import basic_types_pb2, timestamp_pb2

def generate_transaction_id(account_id_proto):
    current_time = timestamp_pb2.Timestamp()
    current_time.seconds = int(time.time())
    current_time.nanos = int((time.time() - current_time.seconds) * 1e9)

    transaction_id = basic_types_pb2.TransactionID()
    transaction_id.accountID.CopyFrom(account_id_proto)
    transaction_id.transactionValidStart.CopyFrom(current_time)
    transaction_id.scheduled = False

    return transaction_id
