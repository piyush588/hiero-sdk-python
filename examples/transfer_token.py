import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.client.network import Network
from src.tokens.token_id import TokenId
from src.transaction.transfer_transaction import TransferTransaction

def transfer_tokens():
    network = Network()
    client = Client(network)

    operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
    operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    recipient_id = AccountId.from_string(os.getenv('RECIPIENT_ID'))
    token_id = TokenId.from_string(os.getenv('TOKEN_ID'))
    amount = 1

    client.set_operator(operator_id, operator_key)

    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, operator_id, -amount)
    transfer_tx.add_token_transfer(token_id, recipient_id, amount)

    receipt = client.execute_transaction(transfer_tx)

    if receipt:
        print("Token transfer successful.")
    else:
        print("Token transfer failed.")

if __name__ == "__main__":
    transfer_tokens()
