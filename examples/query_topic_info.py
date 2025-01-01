import os
from dotenv import load_dotenv
from hedera_sdk_python.client.network import Network
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.query.topic_info_query import TopicInfoQuery
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.crypto.private_key import PrivateKey

def query_topic_info():
    operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
    operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    topic_id = TopicId.from_string("0.0.5336794")

    network = Network(network='testnet')
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    query = TopicInfoQuery().set_topic_id(topic_id)

    topic_info = query.execute(client)
    print("Topic Info:", topic_info)

if __name__ == "__main__":
    query_topic_info()
