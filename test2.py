from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.client.network import Network

def create_token():
    network = Network()
    client = Client(network)

    operator_id = AccountId.from_string("0.0.4668437")
    operator_key = PrivateKey.from_string("302e020100300506032b657004220420dae3977894de2f649342eb51c8e8c5cdcb4d7d3b94b764bf33e8fb5de7019749")

    client.set_operator(operator_id, operator_key)

    token_tx = TokenCreateTransaction()
    token_tx.token_name = "MyToken"
    token_tx.token_symbol = "MTK"
    token_tx.decimals = 2
    token_tx.initial_supply = 1000
    token_tx.treasury_account_id = operator_id

    receipt = client.execute_transaction(token_tx)

    if receipt:
        print(f"Token created with ID: {receipt.tokenID}")
    else:
        print("Token creation failed.")

if __name__ == "__main__":
    create_token()