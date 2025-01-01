import os
import sys
from dotenv import load_dotenv

from hedera_sdk_python.client.client import Client
from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.crypto.private_key import PrivateKey
from hedera_sdk_python.client.network import Network
from hedera_sdk_python.consensus.topic_delete_transaction import TopicDeleteTransaction

load_dotenv()

def delete_topic():
    network = Network(network='testnet')
    client = Client(network)

    operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
    operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    topic_id = TopicId.from_string(os.getenv('TOPIC_ID'))

    client.set_operator(operator_id, operator_key)

    transaction = (
        TopicDeleteTransaction(topic_id=topic_id)
        .freeze_with(client)
        .sign(operator_key)
    )

    try:
        receipt = transaction.execute(client)
        print(f"Topic {topic_id} deleted successfully.")
    except Exception as e:
        print(f"Topic deletion failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    delete_topic()
