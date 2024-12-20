from hedera_sdk_python.query.query import Query
from hedera_sdk_python.hapi import transaction_get_receipt_pb2, query_pb2
from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.transaction.transaction_id import TransactionId
from hedera_sdk_python.transaction.transaction_receipt import TransactionReceipt
import traceback

class TransactionGetReceiptQuery(Query):
    """
    A query to retrieve the receipt of a specific transaction from the Hedera network.

    This class constructs and executes a query to obtain the receipt of a transaction,
    which includes the transaction's status and other pertinent information.
    """

    def __init__(self):
        """Initializes a new instance of the TransactionGetReceiptQuery class."""
        super().__init__()
        self.transaction_id = None

    def set_transaction_id(self, transaction_id: TransactionId):
        """
        Sets the transaction ID for which to retrieve the receipt.

        Args:
            transaction_id (TransactionId): The ID of the transaction.

        Returns:
            TransactionGetReceiptQuery: The current instance for method chaining.
        """
        self.transaction_id = transaction_id
        return self

    def _make_request(self):
        """
        Constructs the protobuf request for the transaction receipt query.

        Returns:
            Query: The protobuf Query object containing the transaction receipt query.

        Raises:
            ValueError: If the transaction ID is not set.
            Exception: If an error occurs during request construction.
        """
        try:
            if not self.transaction_id:
                raise ValueError("Transaction ID must be set before making the request.")

            query_header = self._make_request_header()
            transaction_get_receipt = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
            transaction_get_receipt.header.CopyFrom(query_header)
            transaction_get_receipt.transactionID.CopyFrom(self.transaction_id.to_proto())

            query = query_pb2.Query()
            if not hasattr(query, 'transactionGetReceipt'):
                raise AttributeError("Query object has no attribute 'transactionGetReceipt'")
            query.transactionGetReceipt.CopyFrom(transaction_get_receipt)

            return query
        except Exception as e:
            print(f"Exception in _make_request: {e}")
            traceback.print_exc()
            raise

    def _get_status_from_response(self, response):
        """
        Extracts the status code from the response header.

        Args:
            response (Response): The response received from the network.

        Returns:
            int: The status code indicating the result of the query.
        """
        header = response.transactionGetReceipt.header
        return header.nodeTransactionPrecheckCode

    def _map_response(self, response):
        """
        Maps the response to a TransactionReceipt object.

        Args:
            response (Response): The response received from the network.

        Returns:
            TransactionReceipt: The transaction receipt extracted from the response.

        Raises:
            Exception: If the transaction receipt is not found in the response.
        """
        if response.transactionGetReceipt and response.transactionGetReceipt.receipt:
            receipt_proto = response.transactionGetReceipt.receipt
            return TransactionReceipt.from_proto(receipt_proto)
        else:
            raise Exception("Transaction receipt not found in the response.")
