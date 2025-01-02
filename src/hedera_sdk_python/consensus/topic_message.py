from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto
from datetime import datetime

class TopicMessage:
    """
    Represents a single message returned from a Hedera Mirror Node subscription.
    """

    def __init__(self, consensus_timestamp, message, running_hash, sequence_number):
        self.consensus_timestamp = consensus_timestamp
        self.message = message or b""
        self.running_hash = running_hash or b""
        self.sequence_number = sequence_number or 0

    @classmethod
    def from_proto(cls, response: mirror_proto.ConsensusTopicResponse) -> "TopicMessage":
        """
        Parse a Mirror Node response into a simpler object.
        """
        return cls(
            consensus_timestamp=response.consensusTimestamp,
            message=response.message,
            running_hash=response.runningHash,
            sequence_number=response.sequenceNumber,
        )

    def __str__(self):
        """
        Returns a nicely formatted string representation of the topic message.
        """
        timestamp = datetime.utcfromtimestamp(self.consensus_timestamp.seconds).strftime('%Y-%m-%d %H:%M:%S UTC')
        message = self.message.decode('utf-8', errors='ignore')
        running_hash = self.running_hash.hex()

        return (
            f"Received Topic Message:\n"
            f"  - Timestamp: {timestamp}\n"
            f"  - Sequence Number: {self.sequence_number}\n"
            f"  - Message: {message}\n"
            f"  - Running Hash: {running_hash}\n"
        )
