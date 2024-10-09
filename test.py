import os
from dotenv import load_dotenv
from sdk.client.client import Client
from sdk.account.account_id import AccountId
from sdk.crypto.private_key import PrivateKey
from sdk.token.token_create_transaction import TokenCreateTransaction
from sdk.client.network import Network

def main():
    load_dotenv()
    operator_id_str = os.getenv('OPERATOR_ID')
    operator_key_str = os.getenv('OPERATOR_KEY')
    
    if operator_id_str and operator_key_str:
        print("Loading operator credentials from .env file.")
        try:
            operator_id = AccountId.from_string(operator_id_str)
            operator_key = PrivateKey.from_string(operator_key_str)
        except Exception as e:
            print(f"Error parsing operator credentials from .env: {e}")
            return
        
    # initialise client
    network = Network()
    client = Client(network)
    client.set_operator(operator_id, operator_key)
    
    # create TokenCreateTransaction
    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.decimals = 2
    token_tx.initial_supply = 1000000
    token_tx.treasury_account_id = operator_id
    
    # execute transaction
    receipt = client.execute_transaction(token_tx)
    
    if receipt:
        print("\nTransaction successfully processed.")
        print(f"Status: {receipt.status}")
        print(f"Transaction Cost: {receipt.cost} tinybars")
        if hasattr(receipt, 'token_id') and receipt.token_id:
            print(f"Created Token ID: {receipt.token_id}")
    else:
        print("\nTransaction failed or receipt not available.")

if __name__ == "__main__":
    main()
