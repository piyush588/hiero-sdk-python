import os
import sys
import time
from dotenv import load_dotenv
from src.client.network import Network
from src.outputs import transaction_get_receipt_pb2, response_code_pb2
from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.tokens.token_associate_transaction import TokenAssociateTransaction
from src.transaction.transfer_transaction import TransferTransaction
from src.tokens.token_id import TokenId


def load_credentials():
    """Load credentials from .env file"""
    load_dotenv()
    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    recipient_id_str = os.getenv('RECIPIENT_ID')
    recipient_key_str = os.getenv('RECIPIENT_KEY')

    if operator_id_str and operator_key_str and recipient_id_str and recipient_key_str:
        try:
            operator_id = AccountId.from_string(operator_id_str)
            operator_key = PrivateKey.from_string(operator_key_str)
            recipient_id = AccountId.from_string(recipient_id_str)
            recipient_key = PrivateKey.from_string(recipient_key_str)
        except Exception as e:
            print(f"Error parsing credentials: {e}")
            sys.exit(1)
        return operator_id, operator_key, recipient_id, recipient_key
    else:
        print("Missing credentials in .env file.")
        sys.exit(1)


def create_token(client):
    """Create a new token and return its token ID"""
    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.decimals = 2
    token_tx.initial_supply = 5
    token_tx.treasury_account_id = client.operator_account_id
    token_tx.transaction_fee = 10_000_000_000  # Adjust as necessary

    record = client.execute_transaction(token_tx)
    if record:
        receipt = record.receipt
        status = receipt.status
        status_code = response_code_pb2.ResponseCodeEnum.Name(status)
        if status == response_code_pb2.ResponseCodeEnum.SUCCESS:
            if receipt.tokenID and receipt.tokenID.tokenNum != 0:
                token_id = receipt.tokenID
                formatted_token_id = f"{token_id.shardNum}.{token_id.realmNum}.{token_id.tokenNum}"
                print(f"Token creation successful. Token ID: {formatted_token_id}")
                return token_id
            else:
                print("Token creation failed: Token ID not returned in receipt.")
                sys.exit(1)
        else:
            print(f"Token creation failed with status: {status_code}")
            sys.exit(1)
    else:
        print("Token creation failed: No record returned.")
        sys.exit(1)


def associate_token(client, recipient_id, recipient_key, token_id):
    """Associate the created token with the recipient account"""

    client.set_operator(recipient_id, recipient_key)

    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = recipient_id
    associate_tx.token_ids = [token_id]
    associate_tx.transaction_fee = 10_000_000_000

    receipt = client.execute_transaction(associate_tx)

    if receipt:
        print("Token association successful.")
    else:
        print("Token association failed.")
        sys.exit(1)


def transfer_token(client, recipient_id, token_id):
    """Transfer the created token to the recipient"""
    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, client.operator_account_id, -1)
    transfer_tx.add_token_transfer(token_id, recipient_id, 1)
    transfer_tx.transaction_fee = 10_000_000_000

    receipt = client.execute_transaction(transfer_tx)

    if receipt:
        print("Token transfer successful.")
    else:
        print("Token transfer failed.")
        sys.exit(1)


def main():
    operator_id, operator_key, recipient_id, recipient_key = load_credentials()
    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    token_id = create_token(client)
    associate_token(client, recipient_id, recipient_key, token_id)
    transfer_token(client, recipient_id, token_id)

if __name__ == "__main__":
    main()
