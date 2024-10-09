import random
from sdk.account.account_id import AccountId
from sdk.outputs import transaction_get_receipt_pb2
from sdk.outputs import transaction_get_receipt_pb2_grpc

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
        # select a node at random
        return random.choice(self.nodes)
    
    def get_transaction_receipt(self, transaction_id):
    # create a stub for TransactionReceiptService
        receipt_stub = transaction_get_receipt_pb2_grpc.TransactionReceiptServiceStub(
            grpc.insecure_channel(self.node_address)
        )
        
        # build TransactionGetReceipt query
        query = transaction_get_receipt_pb2.TransactionGetReceiptQuery()
        query.header.node_account_id.CopyFrom(self.node_account_id.to_proto())
        query.transaction_id.CopyFrom(transaction_id)
        
        # execute the query
        response = receipt_stub.getReceipt(query)
        
        return response
    
    @property
    def node_account_id(self):
        # return AccountId 
        return self._node_account_id

    @node_account_id.setter
    def node_account_id(self, value):
        self._node_account_id = value
