from src.outputs import transaction_get_receipt_pb2, query_pb2, query_header_pb2


class TransactionGetReceiptQuery:
    """
    Represents a query to retrieve the receipt of a specific transaction.

    This query is used to check the status and result of a previously submitted transaction.

    Attributes:
        transaction_id (TransactionID): The ID of the transaction to query.
    """

    def __init__(self):
        """
        Initializes the TransactionGetReceiptQuery with no transaction ID.
        """
        self.transaction_id = None

    def execute(self, client, timeout=60):
        """
        Executes the transaction receipt query using the provided client.

        Args:
            client (Client): The client instance to use for sending the query.
            timeout (int, optional): Timeout for the query in seconds. Defaults to 60.

        Returns:
            TransactionReceiptProto: The protobuf receipt of the transaction.

        Raises:
            ValueError: If the transaction ID is not set.
            Exception: If no response is received or the receipt is not found in the response.
        """
        if not self.transaction_id:
            raise ValueError("Transaction ID must be set before executing the query.")

        query_header = query_header_pb2.QueryHeader()

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
