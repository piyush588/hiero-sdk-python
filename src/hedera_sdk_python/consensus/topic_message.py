from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto

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
            sequence_number=response.sequenceNumber
        )

    def __str__(self):
        return (
            f"TopicMessage("
            f"timestamp={self.consensus_timestamp}, "
            f"sequence={self.sequence_number}, "
            f"message={self.message}, "
            f"running_hash={self.running_hash}"
            f")"
        )
