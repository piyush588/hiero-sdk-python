# network.py

import grpc
import random
from src.account.account_id import AccountId


class Network:
    def __init__(self, nodes=None):
        if nodes is None:
            # default to testnet nodes if none are provided
            self.nodes = [
                ("0.testnet.hedera.com:50211", AccountId.from_string("0.0.3")),
                ("1.testnet.hedera.com:50211", AccountId.from_string("0.0.4")),
                ("2.testnet.hedera.com:50211", AccountId.from_string("0.0.5")),
                ("3.testnet.hedera.com:50211", AccountId.from_string("0.0.6")),
            ]
        else:
            self.nodes = nodes

        self.select_node()

    def select_node(self):
        # Select a node at random and update instance variables
        self.node_address, self.node_account_id = random.choice(self.nodes)
