import os
import sys
import binascii
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

def create_token(client, operator_id, operator_key):
    """Create a new token and return its TokenId instance."""
    transaction = (
        TokenCreateTransaction()
        .set_token_name("ExampleToken")
        .set_token_symbol("EXT")
        .set_decimals(2)
        .set_initial_supply(1000)
        .set_treasury_account_id(operator_id)
        .freeze_with(client)
    )

    transaction.sign(operator_key)

    try:
        receipt = transaction.execute(client)
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
    transaction = (
        TokenAssociateTransaction()
        .set_account_id(recipient_id)
        .add_token_id(token_id)
        .freeze_with(client)
        .sign(client.operator_private_key)  # sign with operator's key (payer)
        .sign(recipient_key)                # sign with recipient's key
    )

    try:
        receipt = transaction.execute(client)
        print("Token association successful.")
    except Exception as e:
        print(f"Token association failed: {str(e)}")
        sys.exit(1)

def transfer_token(client, recipient_id, token_id):
    """Transfer the specified token to the recipient account."""
    transaction = (
        TransferTransaction()
        .add_token_transfer(token_id, client.operator_account_id, -1)
        .add_token_transfer(token_id, recipient_id, 1)
        .freeze_with(client)
        .sign(client.operator_private_key)
    )

    try:
        receipt = transaction.execute(client)
        print("Token transfer successful.")
    except Exception as e:
        print(f"Token transfer failed: {str(e)}")
        sys.exit(1)

def main():
    operator_id, operator_key, recipient_id, recipient_key = load_credentials()

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    token_id = create_token(client, operator_id, operator_key)

    associate_token(client, recipient_id, recipient_key, token_id)

    transfer_token(client, recipient_id, token_id)

if __name__ == "__main__":
    main()
