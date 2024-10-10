import grpc
from src.account.account_id import AccountId
from src.outputs import transaction_get_receipt_pb2
from src.outputs import crypto_service_pb2_grpc 
from src.outputs import query_pb2
from src.outputs import query_header_pb2
from src.outputs import response_code_pb2
from src.outputs import basic_types_pb2 
import time
import random

class Network:
    def __init__(self, nodes=None):
        if nodes is None:
            # default to testnet nodes if none are provided
            self.nodes = [
                ("0.testnet.hedera.com:50211", AccountId.from_string("0.0.3")),
                ("1.testnet.hedera.com:50211", AccountId.from_string("0.0.4")),
                ("2.testnet.hedera.com:50211", AccountId.from_string("0.0.5")),
                ("3.testnet.hedera.com:50211", AccountId.from_string("0.0.6")),
            ]
        else:
            self.nodes = nodes

        # select node
        self.node_address, self.node_account_id = self.select_node()

    def select_node(self):
        # Select a node at random and update instance variables
        self.node_address, self._node_account_id = random.choice(self.nodes)
        return self.node_address, self._node_account_id
    
    def get_transaction_receipt(self, transaction_id):
        channel = grpc.insecure_channel(self.node_address)
        receipt_stub = crypto_service_pb2_grpc.CryptoServiceStub(channel)

        query_header = query_header_pb2.QueryHeader()
        query_header.responseType = query_header_pb2.COST_ANSWER

        transaction_get_receipt_query = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
        transaction_get_receipt_query.header.CopyFrom(query_header)
        transaction_get_receipt_query.transactionID.CopyFrom(transaction_id)

        query = query_pb2.Query()
        query.transactionGetReceipt.CopyFrom(transaction_get_receipt_query)

        response = receipt_stub.getTransactionReceipts(query)

        precheck_code = response.transactionGetReceipt.header.nodeTransactionPrecheckCode
        if precheck_code != response_code_pb2.OK:
            raise Exception(f"Error fetching receipt: {response_code_pb2.ResponseCodeEnum.Name(precheck_code)}")

        receipt = response.transactionGetReceipt.receipt

        return receipt

    @property
    def node_account_id(self):
        # return AccountId 
        return self._node_account_id

    @node_account_id.setter
    def node_account_id(self, value):
        self._node_account_id = value
