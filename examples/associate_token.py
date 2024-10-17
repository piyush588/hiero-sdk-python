import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.client.network import Network
from src.tokens.token_id import TokenId
from src.tokens.token_associate_transaction import TokenAssociateTransaction

def associate_token():
    network = Network()
    client = Client(network)

    operator_id = AccountId.from_string(os.getenv('RECIPIENT_ID'))
    operator_key = PrivateKey.from_string(os.getenv('RECIPIENT_KEY'))
    token_id = TokenId.from_string(os.getenv('TOKEN_ID'))

    client.set_operator(operator_id, operator_key)
    
    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = operator_id
    associate_tx.token_ids = [token_id]

    receipt = client.execute_transaction(associate_tx)

    if receipt:
        print(f"Token associated successfully with account: {operator_id}")
    else:
        print("Token association failed.")

if __name__ == "__main__":
    associate_token()