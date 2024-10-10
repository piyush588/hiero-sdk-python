import os
import sys

from dotenv import load_dotenv
from src.client.client import Client
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from src.crypto.private_key import PrivateKey
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.client.network import Network

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def main():
    load_dotenv()
    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    token_id_str = os.getenv('TOKEN_ID')

    if operator_id_str and operator_key_str and token_id_str:
        print("Loading operator credentials from .env file.")
        try:
            operator_id = AccountId.from_string(operator_id_str)
            operator_key = PrivateKey.from_string(operator_key_str)
            token_id = TokenId.from_string(token_id_str)
        except Exception as e:
            print(f"Error parsing credentials from .env: {e}")
            return
    else:
        print("Operator credentials or TOKEN_ID not found in .env file.")
        return

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = operator_id  
    associate_tx.token_ids = [token_id]
    associate_tx.transaction_fee = 1_000_000_000  

    # execute tx
    receipt = client.execute_transaction(associate_tx)

    if receipt:
        print("Token association successful.")
        print(receipt)
    else:
        print("\nToken association failed or receipt not available.")

if __name__ == "__main__":
    main()
