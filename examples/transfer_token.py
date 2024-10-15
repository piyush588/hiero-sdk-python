import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# clear env vars
os.environ.pop('OPERATOR_ID', None)
os.environ.pop('OPERATOR_KEY', None)
os.environ.pop('RECIPIENT_ID', None)
os.environ.pop('RECIPIENT_KEY', None)

from dotenv import load_dotenv

# import classes and modules
from src.client.client import Client
from src.client.network import Network
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_id import TokenId
from src.transaction.transfer_transaction import TransferTransaction
from src.outputs import response_code_pb2

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
    # load credentials
    operator_id, operator_key, recipient_id, token_id = load_credentials()

    # initialize client
    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    # create tx
    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, operator_id, -1)  
    transfer_tx.add_token_transfer(token_id, recipient_id, 1) 
    transfer_tx.transaction_fee = 10_000_000_000

    # execute tx
    record = client.execute_transaction(transfer_tx)
    if not record:
        print("Transfer failed or record not available.")
        sys.exit(1)

    # retrieve receipt from record
    receipt = record.receipt
    status = receipt.status
    status_code = response_code_pb2.ResponseCodeEnum.Name(status)

    if status != response_code_pb2.ResponseCodeEnum.SUCCESS:
        print(f"Token transfer failed with status: {status_code}")
        sys.exit(1)

    print("Transfer successful.")

if __name__ == "__main__":
    main()