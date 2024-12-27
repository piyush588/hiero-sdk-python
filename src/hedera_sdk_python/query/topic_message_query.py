import time
import threading
from datetime import datetime
from typing import Optional, Callable

from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto
from hedera_sdk_python.hapi import basic_types_pb2, timestamp_pb2


class TopicMessageQuery:
    """
    A query to subscribe to messages from a specific HCS topic, via a mirror node.
    """

    def __init__(self):
        self._topic_id = None
        self._start_time = None
        self._end_time = None
        self._limit = None

    def set_topic_id(self, shard: int, realm: int, topic: int):
        self._topic_id = basic_types_pb2.TopicID(
            shardNum=shard,
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

    def subscribe(
        self,
        client,
        on_message: Callable[[mirror_proto.ConsensusTopicResponse], None],
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

        request = mirror_proto.ConsensusTopicQuery(
            topicID=self._topic_id
        )
        if self._start_time:
            request.consensusStartTime.CopyFrom(self._start_time)
        if self._end_time:
            request.consensusEndTime.CopyFrom(self._end_time)
        if self._limit is not None:
            request.limit = self._limit

        def run_stream():
            try:
                message_stream = client.mirror_stub.subscribeTopic(request)
                for message in message_stream:
                    on_message(message)
            except Exception as e:
                if on_error:
                    on_error(e)

        thread = threading.Thread(target=run_stream, daemon=True)
        thread.start()
