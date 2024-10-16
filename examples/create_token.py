
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
from src.client.client import Client
from src.client.network import Network
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.tokens.token_id import TokenId
from src.outputs import response_code_pb2

def load_credentials():
    """Load operator credentials from environment variables."""
    load_dotenv()

    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')

    if not operator_id_str or not operator_key_str:
        print("Operator credentials not found in environment variables.")
        sys.exit(1)

    try:
        operator_id = AccountId.from_string(operator_id_str)
        operator_key = PrivateKey.from_string(operator_key_str)
    except Exception as e:
        print(f"Error parsing operator credentials: {e}")
        sys.exit(1)

    return operator_id, operator_key

def main():
    # load operator credentials
    operator_id, operator_key = load_credentials()

    # initialize client
    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    # create tx
    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.decimals = 2
    token_tx.initial_supply = 1
    token_tx.treasury_account_id = operator_id
    token_tx.transaction_fee = 10_000_000_000  # Adjust as necessary

    # execute tx
    record = client.execute_transaction(token_tx)
    if not record:
        print("Transaction failed or record not available.")
        sys.exit(1)

    # retrieve receipt from record
    receipt = record.receipt
    status = receipt.status
    status_code = response_code_pb2.ResponseCodeEnum.Name(status)

    if status != response_code_pb2.ResponseCodeEnum.SUCCESS:
        print(f"Token creation failed with status: {status_code}")
        sys.exit(1)

    if not receipt.tokenID or receipt.tokenID.tokenNum == 0:
        print("Token creation failed: Token ID not returned in receipt.")
        sys.exit(1)

    # get token Id from receipt
    token_id = TokenId(
        shard=receipt.tokenID.shardNum,
        realm=receipt.tokenID.realmNum,
        num=receipt.tokenID.tokenNum
    )

    print(f"Token creation successful. Token ID: {token_id}")

if __name__ == "__main__":
    main()