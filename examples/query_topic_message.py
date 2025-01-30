import os
import time
from datetime import datetime
from dotenv import load_dotenv

from hedera_sdk_python import (
    Network,
    Client,
    TopicMessageQuery,
)

load_dotenv()

def query_topic_messages():
    network = Network(network='testnet')
    client = Client(network)

    def on_message_handler(topic_message):
        print(f"Received topic message: {topic_message}")

    def on_error_handler(e):
        print(f"Subscription error: {e}")
        if "Stream removed" in str(e):
            print("Reconnecting due to stream removal...")
            query_topic_messages()

    query = TopicMessageQuery(
        topic_id=os.getenv('TOPIC_ID'),
        start_time=datetime.utcnow(),
        limit=0,
        chunking_enabled=True
    )

    query.subscribe(
        client,
        on_message=on_message_handler,
        on_error=on_error_handler
    )

    print("Subscription started. Waiting for messages...")
    while True:
        time.sleep(10)

if __name__ == "__main__":
    query_topic_messages()
