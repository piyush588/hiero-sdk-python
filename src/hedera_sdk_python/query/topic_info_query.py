from hedera_sdk_python.query.query import Query
from hedera_sdk_python.hapi import query_pb2, consensus_get_topic_info_pb2
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.consensus.topic_info import TopicInfo 

class TopicInfoQuery(Query):
    """
    A query to retrieve information about a specific Hedera topic.
    """

    def __init__(self):
        super().__init__()
        self.topic_id = None

    def set_topic_id(self, topic_id: TopicId):
        self.topic_id = topic_id
        return self

    def _make_request(self):
        if not self.topic_id:
            raise ValueError("Topic ID must be set before making the request.")

        query_header = self._make_request_header()

        topic_info_query = consensus_get_topic_info_pb2.ConsensusGetTopicInfoQuery()
        topic_info_query.header.CopyFrom(query_header)
        topic_info_query.topicID.CopyFrom(self.topic_id.to_proto())

        query = query_pb2.Query()
        query.consensusGetTopicInfo.CopyFrom(topic_info_query)

        return query

    def _get_status_from_response(self, response):
        """
        Must read nodeTransactionPrecheckCode from response.consensusGetTopicInfo.header
        """
        return response.consensusGetTopicInfo.header.nodeTransactionPrecheckCode

    def _map_response(self, response):
        """
        Return a TopicInfo instance built from the protobuf
        """
        if not response.consensusGetTopicInfo.topicInfo:
            raise Exception("No topicInfo returned in the response.")

        proto_topic_info = response.consensusGetTopicInfo.topicInfo
        return TopicInfo.from_proto(proto_topic_info)
