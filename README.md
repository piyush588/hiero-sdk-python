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
pytest ./tests 
```

To run one script testing all capabilities of the SDK, use the following command:
```
python test.py
```

#### Output:
```
Token creation successful. Token ID: 0.0.5002222
Token association successful.
Token transfer successful.
```


## Usage

Below are examples of how to use the SDK for creating tokens, associating them with accounts, and transferring tokens (also see 'examples' directiory)

### Creating a Token

```
transaction = (
        TokenCreateTransaction()
        .set_token_name("MyToken")
        .set_token_symbol("MTK")
        .set_decimals(2)
        .set_initial_supply(10)
        .set_treasury_account_id(operator_id)
        .freeze_with(client)
        .sign(operator_key)
    )
```

### Associating a Token

```
transaction = (
        TokenAssociateTransaction()
        .set_account_id(recipient_id)
        .add_token_id(token_id)
        .freeze_with(client)
        .sign(recipient_key)
    )
```

### Transfering a Token

```
    transaction = (
        TransferTransaction()
        .add_token_transfer(token_id, operator_id, -amount)
        .add_token_transfer(token_id, recipient_id, amount)
        .freeze_with(client)
        .sign(operator_key)
    )
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
