import time
import threading
from datetime import datetime
from typing import Optional, Callable, Union
from hedera_sdk_python.consensus.topic_message import TopicMessage
from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto
from hedera_sdk_python.hapi.services import basic_types_pb2, timestamp_pb2
from hedera_sdk_python.consensus.topic_message import TopicMessage
from hedera_sdk_python.consensus.topic_id import TopicId

class TopicMessageQuery:
    """
    A query to subscribe to messages from a specific HCS topic, via a mirror node.
    """

    def __init__(self):
        self._topic_id = None
        self._start_time = None
        self._end_time = None
        self._limit = None
        self._chunking_enabled = False

    def set_topic_id(self, shard_or_str: Union[int, str], realm: int = None, topic: int = None):
        """
        If called with a string like "0.0.12345":
          parse it into (shard, realm, topic).
        Otherwise, accept (shard, realm, topic) as three separate ints.
        """
        if isinstance(shard_or_str, TopicId):
            self._topic_id = shard_or_str.to_proto()
        elif isinstance(shard_or_str, str):
            parts = shard_or_str.strip().split(".")
            if len(parts) != 3:
                raise ValueError(f"Invalid topic ID string: {shard_or_str}")
            shard_num, realm_num, topic_num = map(int, parts)
            self._topic_id = basic_types_pb2.TopicID(
                shardNum=shard_num,
                realmNum=realm_num,
                topicNum=topic_num
            )
        else:
            if realm is None or topic is None:
                raise TypeError("set_topic_id() missing realm/topic arguments")
            self._topic_id = basic_types_pb2.TopicID(
                shardNum=shard_or_str,
                realmNum=realm,
                topicNum=topic
            )
        return self

    def set_start_time(self, dt: datetime):
        """
        Only receive messages with a consensus timestamp >= dt.
        """
        seconds = int(dt.timestamp())
        nanos = int((dt.timestamp() - seconds) * 1e9)
        self._start_time = timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
        return self

    def set_end_time(self, dt: datetime):
        """
        Only receive messages with a consensus timestamp < dt.
        """
        seconds = int(dt.timestamp())
        nanos = int((dt.timestamp() - seconds) * 1e9)
        self._end_time = timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
        return self

    def set_limit(self, limit: int):
        """
        Receive at most `limit` messages, then end the subscription.
        """
        self._limit = limit
        return self

    def set_chunking_enabled(self, enabled: bool):
        """
        For compatibility. Currently a no-op in this example.
        """
        self._chunking_enabled = enabled
        return self

    def subscribe(
        self,
        client,
        on_message: Callable[[TopicMessage], None], 
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        """
        Opens a streaming subscription to the mirror node in the given client, calling on_message()
        for each received message. Returns immediately, streaming in a background thread.
        """

        if not self._topic_id:
            raise ValueError("Topic ID must be set before subscribing.")
        if not client.mirror_stub:
            raise ValueError("Client has no mirror_stub. Did you configure a mirror node address?")

        request = mirror_proto.ConsensusTopicQuery(topicID=self._topic_id)
        if self._start_time:
            request.consensusStartTime.CopyFrom(self._start_time)
        if self._end_time:
            request.consensusEndTime.CopyFrom(self._end_time)
        if self._limit is not None:
            request.limit = self._limit

        def run_stream():
            try:
                message_stream = client.mirror_stub.subscribeTopic(request)
                for response in message_stream:
                    msg_obj = TopicMessage.from_proto(response) 
                    on_message(msg_obj)
            except Exception as e:
                if on_error:
                    on_error(e)

        thread = threading.Thread(target=run_stream, daemon=True)
        thread.start()

