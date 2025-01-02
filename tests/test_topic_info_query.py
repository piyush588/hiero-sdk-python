import pytest
from unittest.mock import MagicMock
from hedera_sdk_python.query.topic_info_query import TopicInfoQuery
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.hapi.services import basic_types_pb2, consensus_get_topic_info_pb2
from hedera_sdk_python.hapi.services.consensus_topic_info_pb2 import ConsensusTopicInfo
from hedera_sdk_python.hapi.services.response_header_pb2 import ResponseHeader


@pytest.fixture
def mock_topic_info_response():
    """Fixture to provide a mock response for the topic info query."""
    topic_info = ConsensusTopicInfo(
        memo="Test topic",
        runningHash=b"\x00" * 48,
        sequenceNumber=10
    )
    response = consensus_get_topic_info_pb2.ConsensusGetTopicInfoResponse(
        header=ResponseHeader(nodeTransactionPrecheckCode=0),
        topicInfo=topic_info
    )
    return response


def test_topic_info_query(mock_topic_info_response):
    """
    Test the TopicInfoQuery with a mocked response.
    """
    topic_id = TopicId(0, 0, 1234)

    query = TopicInfoQuery().set_topic_id(topic_id)

    query.node_account_ids = [MagicMock()]
    query._make_request = MagicMock(return_value="mock_request")
    query._get_status_from_response = MagicMock(return_value=0)  
    query._map_response = MagicMock(return_value=mock_topic_info_response.topicInfo)

    mock_client = MagicMock(spec=Client)
    mock_client.send_query = MagicMock(return_value=mock_topic_info_response)

    topic_info = query.execute(mock_client)

    assert topic_info.memo == "Test topic"
    assert topic_info.runningHash == b"\x00" * 48
    assert topic_info.sequenceNumber == 10
    print("Test passed: TopicInfoQuery works as expected.")
