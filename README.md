# Hiero SDK in Python

This is a Python SDK for interacting with the Hedera Hashgraph platform. It allows developers to:

- Manage Token Transactions like Create, Mint Fungible, Mint Non-Fungible, Associate, Dissociate, Transfer, Freeze & Delete
- Manage Consensus Transactions like Topic Create, Update, Delete
- Submit Topic Messages
- Query Account Balance, Transaction Receipts, Topic Infos and Messages

## Table of Contents

- [Installation](#installation)
  - [Installing from PyPI](#installing-from-pypi)
  - [Installing from Source](#installing-from-source)
  - [Local Editable Installation](#local-editable-installation)
- [Environment Setup](#environment-setup)
- [Running Tests](#running-tests)
- [Contributing](#contributing)

## Installation

### Installing from PyPI

The latest release of this SDK is published to PyPI. You can install it with:

```
pip install --upgrade pip
pip install hiero_sdk_python
```

This will pull down a stable release along with the required dependencies.


### Installing from Source

You can also clone the repo and install dependencies using uv:

1. Install `uv`:

`uv` is an ultra-fast Python package and project manager. It replaces `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`,
`virtualenv`, and more.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If on macOS, you can also install `uv` using Homebrew:

```bash
brew install uv
```

Other installation methods can be found [here](https://docs.astral.sh/uv/getting-started/installation/).

2. Clone this repository:

```bash
git clone https://github.com/hiero-ledger/hiero_sdk_python.git
cd hiero-sdk-python
```

3. Install dependencies:

One of the really nice features of `uv` is that it will download and manage the correct version of python and build
with the correct version of python based on the `.python-version`  file in the project. This means you don't have to
worry about managing multiple versions of python on your machine!

```bash
uv sync
sh generate_proto.sh
```

To update to a newer version of the protobuf libraries, edit the `generate_proto.py` file and change the version number
and then rerun it.


### Local Editable Installation

For active development, you can install the repo in editable mode. That way, changes in your local code are immediately reflected when you import:

```
git clone https://github.com/hiero-ledger/hiero-sdk-python.git
cd hiero-sdk-python
pip install --upgrade pip
pip install -e .
```

Now you can run example scripts like python `examples/account_create.py`, and it will import from your local hiero_sdk_python code.


## Environment Setup

Before using the SDK, you need to configure your environment variables for the operator account and other credentials.
Create a .env file in the root of your project with the following (replace with your environment variables):

```
OPERATOR_ID=0.0.1234xx
OPERATOR_KEY=302e020100300506032b657004220420...
ADMIN_KEY=302a300506032b65700321009308ecfdf...
SUPPLY_KEY =302a300506032b6570032100c5e4af5..."
FREEZE_KEY=302a300306072b65700321009308ecfdf...
RECIPIENT_ID=0.0.789xx
TOKEN_ID=0.0.100xx
TOPIC_ID=0.0.200xx
FREEZE_ACCOUNT_ID=0.0.100
NETWORK=testnet
```

A [sample .env](.env.example) file is provided in the root of this project. If you do not have an account on
the Hedera testnet, you can easily get one from the [Hedera Portal](https://portal.hedera.com/). Learn more about
testnet [here](https://docs.hedera.com/guides/testnet).

## Running Tests

To run the test suite for the SDK, use the following command:
```
uv run pytest 
```

The test file in the root of this project will be automatically run when pushing onto a branch.
This is done by running 'Hedera Solo'. Read more about it here:

- [Github Marketplace](https://github.com/marketplace/actions/hedera-solo)
- [Blog Post by Hendrik Ebbers](https://dev.to/hendrikebbers/ci-for-hedera-based-projects-2nja)

#### Output:
```
Account creation successful. New Account ID: 0.0.5025xxx
New Account Private Key: 228a06c363b0eb328434d51xxx...
New Account Public Key: 8f444e36e8926def492adxxx...
Token creation successful. Token ID: 0.0.5025xxx
Token association successful.
Token dissociation successful.
Token minting successful.
Token transfer successful.
Token freeze successful.
Token deletion successful.
Topic creation successful.
Topic Message submitted.
Topic update successful.
Topic deletion successful.
```

## Contributing

Contributions are welcome! Please follow these steps:

    1. Fork this repository.
    2. Create a new branch with your feature or fix.
    3. Make your changes and ensure the tests pass.
    3. Submit a pull request.

Please ensure all new code is covered by unit tests.

## Versioning and Release Strategy

We use semantic versioning for this project, following the format:

```
MAJOR.MINOR.PATCH
```
    MAJOR: Breaking changes
    MINOR: New features, but backwards-compatible
    PATCH: Bug fixes and other minor changes

Releases to PyPI should ideally increment the version according to these guidelines.
Branching, Committing, and Merging
Branching

We follow a trunk-based development approach. Branches are usually named to reflect the intent:

`feature/...` for new features
`fix/...` for bug fixes

The main branch should always be stable and production-ready.
Committing

We use commit types like feat, fix, docs, chore, test, refactor, style to categorize changes.

Pull Request titles should include:

`feat: ...`, `fix: ...`, etc.

Individual commit messages within those PRs can be more descriptive and do not necessarily need the prefix, as long as they are clear and meaningful.

## Merging

We recommend squash and merge for PRs, along with GPG key signing. An example of a signed commit might look like:

```
git commit -s -S -m "meaningful commit message"
```

Squashing makes the commit history more concise, and signing ensures that commits are verified. Contributors are encouraged to follow these practices.


## License

This project is licensed under the MIT License.
