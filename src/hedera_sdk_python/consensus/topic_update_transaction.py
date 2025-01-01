from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.transaction.transaction import Transaction
from hedera_sdk_python.hapi import consensus_update_topic_pb2, duration_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2

class TopicUpdateTransaction(Transaction):
    def __init__(self, topic_id, memo="", admin_key=None, submit_key=None, auto_renew_period=7890000, auto_renew_account=None, expiration_time=None):
        super().__init__()
        self.topic_id = topic_id
        self.memo = memo
        self.admin_key = admin_key
        self.submit_key = submit_key
        self.auto_renew_period = auto_renew_period
        self.auto_renew_account = auto_renew_account
        self.expiration_time = expiration_time
        self.transaction_fee = 10_000_000

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for topic update.

        Returns:
            TransactionBody: The protobuf transaction body containing the topic update details.

        Raises:
            ValueError: If required fields are missing.
        """
        if self.topic_id is None:
            raise ValueError("Missing required fields: topic_id")

        transaction_body = self.build_base_transaction_body()
        transaction_body.consensusUpdateTopic.CopyFrom(consensus_update_topic_pb2.ConsensusUpdateTopicTransactionBody(
            topicID=self.topic_id.to_proto(),
            adminKey=self.admin_key.to_proto() if self.admin_key is not None else None,
            submitKey=self.submit_key.to_proto() if self.submit_key is not None else None,
            autoRenewPeriod=duration_pb2.Duration(seconds=self.auto_renew_period),
            autoRenewAccount=self.auto_renew_account.to_proto() if self.auto_renew_account is not None else None,
            expirationTime=self.expiration_time.to_proto() if self.expiration_time is not None else None,
            memo=_wrappers_pb2.StringValue(value=self.memo) if self.memo else None
        ))

        return transaction_body

    def _execute_transaction(self, client, transaction_proto):
        """
        Executes the topic update transaction using the provided client.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt: The receipt from the network after transaction execution.

        Raises:
            Exception: If the transaction submission fails or receives an error response.
        """
        response = client.topic_stub.updateTopic(transaction_proto)

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        receipt = self.get_receipt(client)
        return receipt

    def get_receipt(self, client, timeout=60):
        """
        Retrieves the receipt for the transaction.

        Args:
            client (Client): The client instance.
            timeout (int): Maximum time in seconds to wait for the receipt.

        Returns:
            TransactionReceipt: The transaction receipt from the network.

        Raises:
            Exception: If the transaction ID is not set or if receipt retrieval fails.
        """
        if self.transaction_id is None:
            raise Exception("Transaction ID is not set.")

        receipt = client.get_transaction_receipt(self.transaction_id, timeout)
        return receipt