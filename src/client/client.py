import grpc
import time
from src.proto import (
    token_service_pb2_grpc,
    crypto_service_pb2_grpc,
    basic_types_pb2,
    timestamp_pb2
)
from .network import Network
from src.transaction.transaction_receipt import TransactionReceipt
from src.response_code import ResponseCode
from src.query.transaction_get_receipt_query import TransactionGetReceiptQuery


class Client:
    """
    Represents a client to interact with the Hedera network.

    The Client manages the operator's credentials, network configuration, and handles
    sending queries and transactions to the Hedera network.

    Attributes:
        operator_account_id (AccountId): The account ID of the operator.
        operator_private_key (PrivateKey): The private key of the operator.
        network (Network): The network configuration.
        channel (grpc.Channel): The gRPC channel to communicate with the Hedera network.
        token_stub (TokenServiceStub): The gRPC stub for token-related services.
        crypto_stub (CryptoServiceStub): The gRPC stub for crypto-related services.
    """

    def __init__(self, network=None):
        """
        Initializes the Client with optional network configuration.

        Args:
            network (Network, optional): The network configuration. If None, a default
                Network instance is created.
        """
        self.operator_account_id = None
        self.operator_private_key = None
        if network is None:
            network = Network()
        self.network = network
        self.channel = grpc.insecure_channel(self.network.node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)

    def set_operator(self, account_id, private_key):
        """
        Sets the operator's account ID and private key.

        The operator is the account that signs and pays for transactions.

        Args:
            account_id (AccountId): The account ID of the operator.
            private_key (PrivateKey): The private key of the operator.
        """
        self.operator_account_id = account_id
        self.operator_private_key = private_key

    def generate_transaction_id(self):
        """
        Generates a new transaction ID based on the operator's account ID and current time.

        The transaction ID includes a timestamp and the operator's account ID, ensuring
        uniqueness for each transaction.

        Returns:
            TransactionID: The generated transaction ID.

        Raises:
            ValueError: If the operator account ID is not set.
        """
        if self.operator_account_id is None:
            raise ValueError("Operator account ID must be set to generate transaction ID.")

        current_time = time.time()
        timestamp_seconds = int(current_time)
        timestamp_nanos = int((current_time - timestamp_seconds) * 1e9)

        tx_timestamp = timestamp_pb2.Timestamp(seconds=timestamp_seconds, nanos=timestamp_nanos)

        transaction_id = basic_types_pb2.TransactionID(
            transactionValidStart=tx_timestamp,
            accountID=self.operator_account_id.to_proto()
        )
        return transaction_id

    def get_transaction_receipt(self, transaction_id, max_attempts=10, sleep_seconds=2):
        """
        Retrieves the transaction receipt for a given transaction ID.

        Polls the network until the receipt is available or the maximum number of
        attempts is reached.

        Args:
            transaction_id (TransactionID): The ID of the transaction to retrieve the receipt for.
            max_attempts (int, optional): Maximum number of polling attempts. Defaults to 10.
            sleep_seconds (int, optional): Seconds to wait between polling attempts. Defaults to 2.

        Returns:
            TransactionReceipt: The receipt of the transaction.

        Raises:
            Exception: If the transaction fails or the receipt cannot be retrieved within the maximum attempts.
        """
        for attempt in range(max_attempts):
            try:
                receipt_query = TransactionGetReceiptQuery()
                receipt_query.transaction_id = transaction_id
                receipt_proto = receipt_query.execute(self)
                status = receipt_proto.status

                if status == ResponseCode.SUCCESS:
                    return TransactionReceipt(receipt_proto)
                elif status in (ResponseCode.UNKNOWN, ResponseCode.RECEIPT_NOT_FOUND):
                    time.sleep(sleep_seconds)
                    continue
                else:
                    status_message = ResponseCode.get_name(status)
                    raise Exception(f"Transaction failed with status: {status_message}")
            except Exception as e:
                print(f"Error retrieving transaction receipt: {e}")
                time.sleep(sleep_seconds)
        raise Exception("Exceeded maximum attempts to fetch transaction receipt.")

    def send_query(self, query, timeout=60):
        """
        Sends a query to the network and returns the response.

        Args:
            query (Query): The query to send.
            timeout (int, optional): Timeout for the query in seconds. Defaults to 60.

        Returns:
            QueryResponse: The response from the network.

        Raises:
            None. Exceptions are caught and printed, returning None on failure.
        """
        stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)

        try:
            response = stub.getTransactionReceipts(query, timeout=timeout)
            return response
        except grpc.RpcError as e:
            print(f"gRPC error during query execution: {e}")
            return None

    def _switch_node(self):
        """
        Switches to a new node in the network and updates the gRPC stubs.

        This method selects a new node address from the network configuration and
        updates the gRPC channel and service stubs accordingly.
        """
        self.network.select_node()
        self.channel = grpc.insecure_channel(self.network.node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)
