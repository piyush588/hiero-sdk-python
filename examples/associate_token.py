# associate_token.py

import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
from src.client.client import Client
from src.client.network import Network
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.tokens.token_id import TokenId

def load_credentials():
    """Load operator and recipient credentials and TOKEN_ID from environment variables."""
    load_dotenv()

    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    recipient_id_str = os.getenv('RECIPIENT_ID')
    recipient_key_str = os.getenv('RECIPIENT_KEY')
    token_id_str = os.getenv('TOKEN_ID')

    if not all([operator_id_str, operator_key_str, recipient_id_str, recipient_key_str, token_id_str]):
        print("Required credentials or TOKEN_ID not found in environment variables.")
        sys.exit(1)

    try:
        operator_id = AccountId.from_string(operator_id_str)
        operator_key = PrivateKey.from_string(operator_key_str)
        recipient_id = AccountId.from_string(recipient_id_str)
        recipient_key = PrivateKey.from_string(recipient_key_str)
        token_id = TokenId.from_string(token_id_str)
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        sys.exit(1)

    return operator_id, operator_key, recipient_id, recipient_key, token_id

def main():
    operator_id, operator_key, recipient_id, recipient_key, token_id = load_credentials()

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = recipient_id
    associate_tx.token_ids = [token_id]
    associate_tx.transaction_fee = 10_000_000_000

    try:
        client.execute_transaction(associate_tx, additional_signers=[recipient_key])
        print("Token association successful.")
    except Exception as e:
        print(f"Token association failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
