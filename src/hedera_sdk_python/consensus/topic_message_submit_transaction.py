from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.transaction.transaction import Transaction
from hedera_sdk_python.hapi import consensus_submit_message_pb2, duration_pb2

class TopicMessageSubmitTransaction(Transaction):
    def __init__(self, topic_id, message):
        super().__init__()
        self.topic_id = topic_id
        self.message = message

    def set_topic_id(self, topic_id):
        """
        Sets the topic ID for the message submission.

        Args:
            topic_id (TopicId): The ID of the topic to which the message is submitted.

        Returns:
            TopicMessageSubmitTransaction: This transaction instance (for chaining).
        """
        self._require_not_frozen()
        self.topic_id = topic_id
        return self

    def set_message(self, message):
        """
        Sets the message to submit to the topic.

        Args:
            message (str): The message to submit to the topic.

        Returns:
            TopicMessageSubmitTransaction: This transaction instance (for chaining).
        """
        self._require_not_frozen()
        self.message = message
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for message submission.

        Returns:
            TransactionBody: The protobuf transaction body containing the message submission details.

        Raises:
            ValueError: If required fields are missing.
        """
        transaction_body = self.build_base_transaction_body()
        transaction_body.consensusSubmitMessage.CopyFrom(consensus_submit_message_pb2.ConsensusSubmitMessageTransactionBody(
            topicID=self.topic_id.to_proto(),
            message=bytes(self.message, 'utf-8')
        ))

        return transaction_body

    def _execute_transaction(self, client, transaction_proto):
        """
        Executes the message submit transaction using the provided client.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt: The receipt from the network after transaction execution.

        Raises:
            Exception: If the transaction submission fails or receives an error response.
        """
        response = client.topic_stub.submitMessage(transaction_proto)

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