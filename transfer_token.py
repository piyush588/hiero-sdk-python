import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from dotenv import load_dotenv
from client.client import Client
from account.account_id import AccountId
from tokens.token_id import TokenId
from crypto.private_key import PrivateKey
from transaction.transfer_transaction import TransferTransaction
from client.network import Network

def main():
    load_dotenv()
    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    recipient_id_str = os.getenv('RECIPIENT_ID')
    token_id_str = os.getenv('TOKEN_ID')

    if operator_id_str and operator_key_str and recipient_id_str and token_id_str:
        print("Loading credentials from .env file.")
        try:
            operator_id = AccountId.from_string(operator_id_str)
            operator_key = PrivateKey.from_string(operator_key_str)
            recipient_id = AccountId.from_string(recipient_id_str)
            token_id = TokenId.from_string(token_id_str)
        except Exception as e:
            print(f"Error parsing credentials from .env: {e}")
            return
    else:
        print("Credentials or TOKEN_ID not found in .env file.")
        return

    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)

    transfer_tx = TransferTransaction()
    transfer_tx.add_hbar_transfer(operator_id, -1_000_000_000)  # -10 hbar in tinybars
    transfer_tx.add_hbar_transfer(recipient_id, 1_000_000_000)   # +10 hbar in tinybars

    transfer_tx.add_token_transfer(token_id, operator_id, -100)
    transfer_tx.add_token_transfer(token_id, recipient_id, 100)

    # Sset tx fee
    transfer_tx.transaction_fee = 20_000_000  # Adjust as needed

    # exec tx
    receipt = client.execute_transaction(transfer_tx)

    if receipt:
        print("Transfer successful.")
        print(receipt)
    else:
        print("\nTransfer failed or receipt not available.")

if __name__ == "__main__":
    main()
