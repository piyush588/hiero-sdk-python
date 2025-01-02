import os
import time
from datetime import datetime
from dotenv import load_dotenv

from hedera_sdk_python.client.network import Network
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.query.topic_message_query import TopicMessageQuery

load_dotenv()

def query_topic_messages():
    network = Network(network='testnet')
    client = Client(network)

    def on_message_handler(topic_message):
        print("Received topic message:", topic_message)

    def on_error_handler(e):
        print("Subscription error:", e)

    query = (
        TopicMessageQuery()
        .set_topic_id("0.0.5337028") 
        .set_start_time(datetime.utcnow())
        .set_chunking_enabled(True)
        .set_limit(5)
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
