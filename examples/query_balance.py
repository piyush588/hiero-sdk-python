import os
import sys
import time
from dotenv import load_dotenv

from hedera_sdk_python.account.account_id import AccountId
from hedera_sdk_python.crypto.private_key import PrivateKey
from hedera_sdk_python.client.network import Network
from hedera_sdk_python.client.client import Client
from hedera_sdk_python.account.account_create_transaction import AccountCreateTransaction
from hedera_sdk_python.transaction.transfer_transaction import TransferTransaction
from hedera_sdk_python.query.account_balance_query import CryptoGetAccountBalanceQuery
from hedera_sdk_python.hbar import Hbar
from hedera_sdk_python.response_code import ResponseCode

load_dotenv()

def create_account_and_transfer():
    network = Network(network='testnet')
    client = Client(network)
    operator_id = AccountId.from_string(os.getenv('OPERATOR_ID'))
    operator_key = PrivateKey.from_string(os.getenv('OPERATOR_KEY'))
    client.set_operator(operator_id, operator_key)

    new_account_private_key = PrivateKey.generate()
    new_account_public_key = new_account_private_key.public_key()

    initial_balance = Hbar(10) 
    transaction = (
        AccountCreateTransaction()
        .set_key(new_account_public_key)
        .set_initial_balance(initial_balance)
        .set_account_memo("New Account")
        .freeze_with(client)
    )
    transaction.sign(operator_key)
    receipt = transaction.execute(client)
    new_account_id = receipt.accountId
    print(f"New account created with ID: {new_account_id}")

    balance_query = CryptoGetAccountBalanceQuery().set_account_id(new_account_id)
    balance = balance_query.execute(client)
    print(f"Initial balance of new account: {balance.hbars} hbars")

    transfer_amount = Hbar(5)
    transfer_transaction = (
        TransferTransaction()
        .add_hbar_transfer(operator_id, -transfer_amount.to_tinybars())
        .add_hbar_transfer(new_account_id, transfer_amount.to_tinybars())
        .freeze_with(client)
        .sign(operator_key)
    )
    transfer_receipt = transfer_transaction.execute(client)
    print(f"Transfer transaction status: {ResponseCode.get_name(transfer_receipt.status)}")

    time.sleep(2)

    updated_balance_query = CryptoGetAccountBalanceQuery().set_account_id(new_account_id)
    updated_balance = updated_balance_query.execute(client)
    print(f"Updated balance of new account: {updated_balance.hbars} hbars")

if __name__ == "__main__":
    create_account_and_transfer()