# client.py

import grpc
import time
from ..account.account_id import AccountId
from ..outputs import (
    token_service_pb2_grpc,
    crypto_transfer_pb2,
    crypto_service_pb2_grpc,
    transaction_get_receipt_pb2,
    query_pb2,
    query_header_pb2,
    basic_types_pb2,
    transaction_body_pb2,
    transaction_pb2,
    transaction_contents_pb2,
    transaction_get_record_pb2,
    transaction_contents_pb2
)
from cryptography.hazmat.primitives import serialization
from ..utils import generate_transaction_id
from .network import Network
from ..tokens.token_create_transaction import TokenCreateTransaction
from ..tokens.token_associate_transaction import TokenAssociateTransaction
from ..transaction.transfer_transaction import TransferTransaction
from ..response_code import ResponseCode

class Client:
    def __init__(self, network=None):
        self.operator_account_id = None
        self.operator_private_key = None
        if network is None:
            network = Network()
        self.network = network
        self.channel = grpc.insecure_channel(self.network.node_address)
        self.token_stub = token_service_pb2_grpc.TokenServiceStub(self.channel)
        self.crypto_stub = crypto_service_pb2_grpc.CryptoServiceStub(self.channel)

    def set_operator(self, account_id, private_key):
        self.operator_account_id = account_id
        self.operator_private_key = private_key

    def _create_payment_transaction(self):
        """Creates a signed transaction for query payment."""
        account_id_proto = self.operator_account_id.to_proto()
        transaction_id = generate_transaction_id(account_id_proto)

        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.network.node_account_id.to_proto())
        transaction_body.transactionFee = 0  # Set fee to 0 for free queries
        transaction_body.transactionValidDuration.seconds = 120
        transaction_body.generateRecord = False
        transaction_body.memo = "Query Payment"

        transaction_body_bytes = transaction_body.SerializeToString()

        signature = self.operator_private_key.sign(transaction_body_bytes)

        public_key_bytes = self.operator_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
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

        transaction = transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )

        return transaction

    def get_transaction_receipt(self, transaction_id, max_attempts=10, sleep_seconds=2):
        channel = grpc.insecure_channel(self.network.node_address)
        receipt_stub = crypto_service_pb2_grpc.CryptoServiceStub(channel)

        for attempt in range(max_attempts):
            payment_transaction = self._create_payment_transaction_for_query()

            # build the query header with payment tx
            query_header = query_header_pb2.QueryHeader()
            query_header.payment.CopyFrom(payment_transaction)
            query_header.responseType = query_header_pb2.ResponseType.Value('ANSWER_ONLY')

            # build TransactionGetReceipt query
            transaction_get_receipt_query = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
            transaction_get_receipt_query.header.CopyFrom(query_header)
            transaction_get_receipt_query.transactionID.CopyFrom(transaction_id)

            # build query
            query = query_pb2.Query()
            query.transactionGetReceipt.CopyFrom(transaction_get_receipt_query)

            # execute query
            response = receipt_stub.getTransactionReceipts(query)

            receipt = response.transactionGetReceipt.receipt
            status = receipt.status

            # check if the transaction has reached consensus
            if status == ResponseCode.SUCCESS:
                return receipt
            elif status in (ResponseCode.UNKNOWN, ResponseCode.RECEIPT_NOT_FOUND):
                time.sleep(sleep_seconds)
                continue
            else:
                # handle other status codes
                status_message = ResponseCode.get_name(status)
                raise Exception(f"Transaction failed with status: {status_message}")

        raise Exception("Exceeded maximum attempts to fetch transaction receipt.")
    
    def get_transaction_record(self, transaction_id):
        channel = grpc.insecure_channel(self.network.node_address)
        record_stub = crypto_service_pb2_grpc.CryptoServiceStub(channel)

        # create a payment tx for query
        payment_transaction = self._create_payment_transaction_for_query()

        query_header = query_header_pb2.QueryHeader()
        query_header.payment.CopyFrom(payment_transaction)
        query_header.responseType = query_header_pb2.ResponseType.Value('ANSWER_ONLY')

        transaction_get_record_query = transaction_get_record_pb2.TransactionGetRecordQuery()
        transaction_get_record_query.header.CopyFrom(query_header)
        transaction_get_record_query.transactionID.CopyFrom(transaction_id)
        transaction_get_record_query.include_child_records = False

        query = query_pb2.Query()
        query.transactionGetRecord.CopyFrom(transaction_get_record_query)

        response = record_stub.getTxRecordByTxID(query)

        record = response.transactionGetRecord.transactionRecord
        return record
    
    def _create_payment_transaction_for_query(self):
        """Creates a signed transaction for query payment."""
        account_id_proto = self.operator_account_id.to_proto()
        transaction_id = generate_transaction_id(account_id_proto)

        transaction_body = transaction_body_pb2.TransactionBody()
        transaction_body.transactionID.CopyFrom(transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.network.node_account_id.to_proto())
        transaction_body.transactionFee = 200_000  # Increased fee to 200,000 tinybars
        transaction_body.transactionValidDuration.seconds = 120
        transaction_body.generateRecord = False
        transaction_body.memo = "Query Payment"

        transfer_list = basic_types_pb2.TransferList()
        account_amount = basic_types_pb2.AccountAmount()
        account_amount.accountID.CopyFrom(self.operator_account_id.to_proto())
        account_amount.amount = -200_000  # Deduct fee from operator
        transfer_list.accountAmounts.append(account_amount)

        node_account_amount = basic_types_pb2.AccountAmount()
        node_account_amount.accountID.CopyFrom(self.network.node_account_id.to_proto())
        node_account_amount.amount = 200_000  # Add fee to node account
        transfer_list.accountAmounts.append(node_account_amount)

        crypto_transfer = crypto_transfer_pb2.CryptoTransferTransactionBody()
        crypto_transfer.transfers.CopyFrom(transfer_list)
        transaction_body.cryptoTransfer.CopyFrom(crypto_transfer)

        transaction_body_bytes = transaction_body.SerializeToString()

        signature = self.operator_private_key.sign(transaction_body_bytes)

        public_key_bytes = self.operator_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
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

        transaction = transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )

        return transaction

    def execute_transaction(self, transaction, additional_signers=None, timeout=60):
        if not transaction.transaction_id:
            transaction_id = generate_transaction_id(self.operator_account_id.to_proto())
            transaction.setup_base_transaction(transaction_id, self.network.node_account_id)
        
        transaction.sign(self.operator_private_key)

        if additional_signers:
            for signer in additional_signers:
                transaction.sign(signer)

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

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        transaction_id = transaction.transaction_id
        print(f"Transaction submitted. Transaction ID: {self._format_transaction_id(transaction_id)}")

        receipt = self.get_transaction_receipt(transaction_id)
        if receipt.status != ResponseCode.SUCCESS:
            status_message = ResponseCode.get_name(receipt.status)
            raise Exception(f"Transaction failed with status: {status_message}")

        return receipt

    def _submit_transaction_with_retry(self, transaction_proto, stub_method, max_retries=3):
        response = None
        for attempt in range(max_retries):
            try:
                response = stub_method(transaction_proto)
                if response.nodeTransactionPrecheckCode == ResponseCode.BUSY:
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

    def _format_transaction_id(self, transaction_id):
        account_id = transaction_id.accountID
        valid_start = transaction_id.transactionValidStart
        return f"{account_id.shardNum}.{account_id.realmNum}.{account_id.accountNum}-{valid_start.seconds}.{valid_start.nanos}"
