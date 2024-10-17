# transfer_token.py

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
from src.client.client import Client
from src.client.network import Network
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_id import TokenId
from src.transaction.transfer_transaction import TransferTransaction

def load_credentials():
    """Load operator and recipient credentials and TOKEN_ID from environment variables."""
    load_dotenv()

    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    recipient_id_str = os.getenv('RECIPIENT_ID')
    token_id_str = os.getenv('TOKEN_ID')

    if not all([operator_id_str, operator_key_str, recipient_id_str, token_id_str]):
        print("Required credentials or TOKEN_ID not found in environment variables.")
        sys.exit(1)

    try:
        operator_id = AccountId.from_string(operator_id_str)
        operator_key = PrivateKey.from_string(operator_key_str)
        recipient_id = AccountId.from_string(recipient_id_str)
        token_id = TokenId.from_string(token_id_str)
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        sys.exit(1)

    return operator_id, operator_key, recipient_id, token_id

def main():
    operator_id, operator_key, recipient_id, token_id = load_credentials()

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, operator_id, -1)
    transfer_tx.add_token_transfer(token_id, recipient_id, 1)
    transfer_tx.transaction_fee = 10_000_000_000  # Adjust as necessary

    try:
        client.execute_transaction(transfer_tx)
        print("Transfer successful.")
    except Exception as e:
        print(f"Token transfer failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
