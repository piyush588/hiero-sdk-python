import os
import sys
from dotenv import load_dotenv

from src.client.network import Network
from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.transaction.transfer_transaction import TransferTransaction

# Load environment variables
load_dotenv()

def load_credentials():
    """Load operator and recipient credentials from environment variables."""
    try:
        operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
        operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
        recipient_id = AccountId.from_string(os.getenv('RECIPIENT_ID'))
        recipient_key = PrivateKey.from_string(os.getenv('RECIPIENT_KEY'))
    except Exception as e:
        print(f"Error parsing credentials: {e}")
        sys.exit(1)

    return operator_id, operator_key, recipient_id, recipient_key

def create_token(client):
    """Create a new token and return its TokenId instance."""
    
    token_tx = TokenCreateTransaction()
    token_tx.token_name = os.getenv('TOKEN_NAME', "MyToken")
    token_tx.token_symbol = os.getenv('TOKEN_SYMBOL', "MTK")
    token_tx.decimals = int(os.getenv('TOKEN_DECIMALS', 2))
    token_tx.initial_supply = int(os.getenv('INITIAL_SUPPLY', 5))
    token_tx.treasury_account_id = client.operator_account_id

    try:
        receipt = client.execute_transaction(token_tx)
    except Exception as e:
        print(f"Token creation failed: {str(e)}")
        sys.exit(1)

    if not receipt.tokenId:
        print("Token creation failed: Token ID not returned in receipt.")
        sys.exit(1)

    token_id = receipt.tokenId
    print(f"Token creation successful. Token ID: {token_id}")

    return token_id

def associate_token(client, recipient_id, recipient_key, token_id):
    """Associate the specified token with the recipient account."""

    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = recipient_id
    associate_tx.token_ids = [token_id]

    try:
        client.execute_transaction(associate_tx, additional_signers=[recipient_key])
        print("Token association successful.")
    except Exception as e:
        print(f"Token association failed: {str(e)}")
        sys.exit(1)

def transfer_token(client, recipient_id, token_id):
    """Transfer the specified token to the recipient account."""

    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, client.operator_account_id, -1)
    transfer_tx.add_token_transfer(token_id, recipient_id, 1)

    try:
        client.execute_transaction(transfer_tx)
        print("Token transfer successful.")
    except Exception as e:
        print(f"Token transfer failed: {str(e)}")
        sys.exit(1)

def main():
    operator_id, operator_key, recipient_id, recipient_key = load_credentials()

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    # create new token
    token_id = create_token(client)

    # associate token with recipient account
    associate_token(client, recipient_id, recipient_key, token_id)

    # transfer token to recipient
    transfer_token(client, recipient_id, token_id)

if __name__ == "__main__":
    main()
