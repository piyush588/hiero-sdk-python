from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto
from datetime import datetime

class TopicMessage:
    """
    Represents a single message returned from a Hedera Mirror Node subscription.
    """

    def __init__(self, consensus_timestamp, message, running_hash, sequence_number, 
                 running_hash_version=None, chunk_info=None, chunks=None, transaction_id=None):
        self.consensus_timestamp = consensus_timestamp
        self.message = message or b""
        self.running_hash = running_hash or b""
        self.sequence_number = sequence_number or 0
        self.running_hash_version = running_hash_version
        self.chunk_info = chunk_info
        self.chunks = chunks
        self.transaction_id = transaction_id

    @classmethod
    def from_proto(cls, response: mirror_proto.ConsensusTopicResponse) -> "TopicMessage":
        """
        Parse a Mirror Node response into a simpler object.
        """
        transaction_id = (
            response.chunkInfo.initialTransactionID
            if response.HasField("chunkInfo") and response.chunkInfo.HasField("initialTransactionID")
            else None
        )
        return cls(
            consensus_timestamp=response.consensusTimestamp,
            message=response.message,
            running_hash=response.runningHash,
            sequence_number=response.sequenceNumber,
            running_hash_version=response.runningHashVersion if response.runningHashVersion != 0 else None,
            chunk_info=response.chunkInfo if response.HasField("chunkInfo") else None,
            transaction_id=transaction_id,
        )

    def __str__(self):
        """
        Returns a nicely formatted string representation of the topic message.
        """
        timestamp = datetime.utcfromtimestamp(self.consensus_timestamp.seconds).strftime('%Y-%m-%d %H:%M:%S UTC')
        message = self.message.decode('utf-8', errors='ignore')
        running_hash = self.running_hash.hex()

        formatted_message = (
            f"Received Topic Message:\n"
            f"  - Timestamp: {timestamp}\n"
            f"  - Sequence Number: {self.sequence_number}\n"
            f"  - Message: {message}\n"
            f"  - Running Hash: {running_hash}\n"
        )
        if self.running_hash_version:
            formatted_message += f"  - Running Hash Version: {self.running_hash_version}\n"
        if self.chunk_info:
            formatted_message += f"  - Chunk Info: {self.chunk_info}\n"
        if self.transaction_id:
            formatted_message += f"  - Transaction ID: {self.transaction_id}\n"
        return formatted_message
