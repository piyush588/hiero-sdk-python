from src.query.query import Query
from src.proto import transaction_get_receipt_pb2, query_pb2
from src.response_code import ResponseCode
from src.transaction.transaction_id import TransactionId
from src.transaction.transaction_receipt import TransactionReceipt

class TransactionGetReceiptQuery(Query):
    """
    Represents a query to retrieve the receipt of a specific transaction.
    """

    def __init__(self):
        super().__init__()
        self.transaction_id = None

    def set_transaction_id(self, transaction_id: TransactionId):
        self.transaction_id = transaction_id
        return self

    def _make_request(self):
        """
        Constructs the query request.

        Returns:
            Query: The protobuf Query object.

        Raises:
            ValueError: If the transaction ID is not set.
        """
        print("TransactionGetReceiptQuery: _make_request called")
        if not self.transaction_id:
            raise ValueError("Transaction ID must be set before making the request.")

        query_header = self._make_request_header()
        transaction_get_receipt = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
        transaction_get_receipt.header.CopyFrom(query_header)
        transaction_get_receipt.transactionID.CopyFrom(self.transaction_id.to_proto())
        query = query_pb2.Query()
        query.transactionGetReceipt.CopyFrom(transaction_get_receipt)
        return query

    def _get_status_from_response(self, response):
        header = response.transactionGetReceipt.header
        return header.nodeTransactionPrecheckCode

    def _map_response(self, response):
        if response.transactionGetReceipt and response.transactionGetReceipt.receipt:
            receipt_proto = response.transactionGetReceipt.receipt
            return TransactionReceipt.from_proto(receipt_proto)
        else:
            raise Exception("Transaction receipt not found in the response.")
