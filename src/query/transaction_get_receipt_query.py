from src.outputs import transaction_get_receipt_pb2, query_pb2, response_pb2

class TransactionGetReceiptQuery:
    def __init__(self):
        self.transaction_id = None

    def execute(self, client, timeout=60):
        if not self.transaction_id:
            raise ValueError("Transaction ID must be set before executing the query.")

        query_header = query_pb2.QueryHeader()

        transaction_get_receipt = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
        transaction_get_receipt.header.CopyFrom(query_header)
        transaction_get_receipt.transactionID.CopyFrom(self.transaction_id)

        query = query_pb2.Query()
        query.transactionGetReceipt.CopyFrom(transaction_get_receipt)

        response = client.send_query(query, timeout=timeout)

        if response is None:
            raise Exception("No response received from the network.")

        if response.transactionGetReceipt:
            receipt = response.transactionGetReceipt.receipt
            return receipt
        else:
            raise Exception("Transaction receipt not found in the response.")