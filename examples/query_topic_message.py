import os
from dotenv import load_dotenv

from hedera_sdk_python.client.network import Network
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.consensus.topic_id import TopicId
from hedera_sdk_python.query.topic_message_query import TopicMessageQuery
from datetime import datetime
import time

load_dotenv()

def query_topic_messages():
    
    network = Network(network='testnet') 
    client = Client(network)

    def on_message_handler(msg):
        print("Received topic message:", msg)

    def on_error_handler(e):
        print("Subscription error:", e)

    query = (
        TopicMessageQuery()
        .set_topic_id("0.0.12345")
        .set_start_time(datetime.utcnow())
        .set_chunking_enabled(True)
    )

    query.subscribe(
        client, 
        on_message=on_message_handler, 
        on_error=on_error_handler
    )

    time.sleep(10)
    print("Done waiting. Exiting.")


if __name__ == "__main__":
    query_topic_messages()
