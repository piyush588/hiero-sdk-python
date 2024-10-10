import grpc
import time
from src.outputs import (
    token_service_pb2_grpc,
    crypto_service_pb2_grpc,
    response_code_pb2,
)
from src.client.network import Network
from src.utils import generate_transaction_id
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.transaction.transfer_transaction import TransferTransaction


class Client:
    def __init__(self, network=None):
        if network is None:
            network = Network()
        self.network = network
        self.operator_account_id = None  
        self.operator_private_key = None
        self.channel = grpc.insecure_channel(self.network.node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)

    def set_operator(self, account_id, private_key):
        self.operator_account_id = account_id.to_proto()
        self.operator_private_key = private_key

    def execute_transaction(self, transaction, timeout=60):
        transaction.transaction_id = generate_transaction_id(self.operator_account_id)
        transaction.node_account_id = self.network.node_account_id.to_proto()
        transaction.sign(self.operator_private_key)

        transaction_proto = transaction.to_proto()

        if isinstance(transaction, TokenCreateTransaction):
            stub_method = self.token_stub.createToken
        elif isinstance(transaction, TokenAssociateTransaction):
            stub_method = self.token_stub.associateTokens
        elif isinstance(transaction, TransferTransaction):
            stub_method = self.crypto_stub.cryptoTransfer
        else:
            raise NotImplementedError("Transaction type not supported.")

        response = self._submit_transaction_with_retry(transaction_proto, stub_method)

        if response.nodeTransactionPrecheckCode != response_code_pb2.ResponseCodeEnum.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = response_code_pb2.ResponseCodeEnum.ResponseCodeEnum.Name(error_code)
            print(f"Error during transaction submission: {error_code} ({error_message})")
            return None

        transaction_id = transaction.transaction_id
        print(f"Transaction submitted. Transaction ID: {self._format_transaction_id(transaction_id)}")

        return self._poll_for_receipt(transaction_id, timeout)

    def _submit_transaction_with_retry(self, transaction_proto, stub_method, max_retries=3):
        """Helper method to submit a transaction with retries in case of a 'BUSY' node."""
        for attempt in range(max_retries):
            try:
                response = stub_method(transaction_proto)
                if response.nodeTransactionPrecheckCode == response_code_pb2.ResponseCodeEnum.BUSY:
                    print(f"Node is busy (attempt {attempt + 1}/{max_retries}), retrying...")
                    self._switch_node()
                    time.sleep(2)
                else:
                    return response
            except grpc.RpcError as e:
                print(f"gRPC error during transaction submission: {e}")
                self._switch_node()
                time.sleep(2)
        return response

    def _switch_node(self):
        """Switch to a new node in the network and update stubs."""
        self.network.select_node()  # Select a new node
        self.channel = grpc.insecure_channel(self.network.node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)

    def _poll_for_receipt(self, transaction_id, timeout):
        """Helper method to poll for transaction receipt within the specified timeout."""
        start_time = time.time()
        receipt = None

        while time.time() - start_time < timeout:
            try:
                receipt = self.network.get_transaction_receipt(transaction_id)
                if receipt:
                    break
            except Exception as e:
                print(f"Error fetching receipt: {e}")
            time.sleep(2)

        if receipt:
            if hasattr(receipt, 'token_id') and receipt.token_id:
                print(f"Created Token ID: {receipt.token_id}")
            return receipt
        else:
            print("Failed to fetch transaction receipt within the timeout period.")
            return None

    def _format_transaction_id(self, transaction_id):
        account_id = transaction_id.accountID
        valid_start = transaction_id.transactionValidStart
        return f"{account_id.shardNum}.{account_id.realmNum}.{account_id.accountNum}-{valid_start.seconds}.{valid_start.nanos}"