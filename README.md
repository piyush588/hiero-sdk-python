# Hedera (Mini) SDK in Python

This is a Python SDK for interacting with the Hedera Hashgraph platform. It allows developers to manage Token transactions like CREATE, ASSOCIATE and TRANSFER.


## Table of Contents

- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running Tests](#running-tests)
- [Usage](#usage)
  - [Creating a Token](#creating-a-token)
  - [Associating a Token](#associating-a-token)
  - [Transferring Tokens](#transferring-tokens)
- [Contributing](#contributing)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/nadineloepfe/hedera_sdk_python.git
cd hedera_sdk_python
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Install the SDK as a Python Package:
```
pip install .
```

## Environment Setup

Before using the SDK, you need to configure your environment variables for the operator account and other credentials. Create a .env file in the root of your project with the following (replace with your environment variables):

```
OPERATOR_ID=0.0.1234xx
OPERATOR_KEY=302e020100300506032b657004220420...
RECIPIENT_ID=0.0.789xx
TOKEN_ID=0.0.100xx
```

## Running Tests

To run the test suite for the SDK, use the following command:
```
python -m unittest discover -s tests
```

To run one script testing all capabilities of the SDK, use the following command:
```
python test.py
```


## Usage

Below are examples of how to use the SDK for creating tokens, associating them with accounts, and transferring tokens (also see 'examples' directiory)

### Creating a Token

```
from src.client.client import Client
from src.account.account_id import AccountId
from src.crypto.private_key import PrivateKey
from src.tokens.token_create_transaction import TokenCreateTransaction
from src.client.network import Network

def create_token():
    network = Network()
    client = Client(network)

    operator_id = AccountId.from_string("0.0.123456")
    operator_key = PrivateKey.from_string("302e020100300506032b657004220420...")

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
```

### Associating a Token

```
from src.tokens.token_associate_transaction import TokenAssociateTransaction

def associate_token(client, account_id, token_id):
    associate_tx = TokenAssociateTransaction()
    associate_tx.account_id = account_id
    associate_tx.token_ids = [token_id]

    receipt = client.execute_transaction(associate_tx)

    if receipt:
        print(f"Token associated successfully with account: {account_id}")
    else:
        print("Token association failed.")
```

### Transfering a Token

```
from src.transaction.transfer_transaction import TransferTransaction

def transfer_tokens(client, token_id, sender_account, recipient_account, amount):
    transfer_tx = TransferTransaction()
    transfer_tx.add_token_transfer(token_id, sender_account, -amount)
    transfer_tx.add_token_transfer(token_id, recipient_account, amount)

    receipt = client.execute_transaction(transfer_tx)

    if receipt:
        print("Token transfer successful.")
    else:
        print("Token transfer failed.")
```

## Contributing

Contributions are welcome! Please follow these steps:

    1. Fork this repository.
    2. Create a new branch with your feature or fix.
    3. Make your changes and ensure the tests pass.
    3. Submit a pull request.

Please ensure all new code is covered by unit tests.

## License

This project is licensed under the MIT License.
