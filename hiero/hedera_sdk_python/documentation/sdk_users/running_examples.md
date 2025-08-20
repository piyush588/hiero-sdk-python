# Hiero Python SDK – Syntax Flexibility

The Hedera SDK in Python supports two distinct syntax styles for creating and executing transactions:

- Pythonic Syntax: Ideal for developers who prefer explicit constructor-style initialization.
- Method Chaining: Provides a fluent API style for chaining methods, commonly used in many SDKs.

You can choose either syntax or even mix both styles in your projects.


## Table of Contents

- [Account Transactions](#account-transactions)
  - [Creating an Account](#creating-an-account)
  - [Updating an Account](#updating-an-account)
  - [Querying Account Balance](#querying-account-balance)
  - [Querying Account Info](#querying-account-info)
  - [Creating a Token](#creating-a-token)
- [Token Transactions](#token-transactions)
  - [Minting a Fungible Token](#minting-a-fungible-token)
  - [Minting a Non-Fungible Token](#minting-a-non-fungible-token)
  - [Associating a Token](#associating-a-token)
  - [Dissociating a Token](#dissociating-a-token)
  - [Transferring Tokens](#transferring-tokens)
  - [Transferring NFTs](#transferring-nfts)
  - [Wiping Tokens](#wiping-tokens)
  - [Deleting a Token](#deleting-a-token)
  - [Freezing a Token](#freezing-a-token)
  - [Unfreezing a Token](#unfreezing-a-token)
  - [Rejecting a Token](#rejecting-a-token)
  - [Rejecting a Non-Fungible Token](#rejecting-a-non-fungible-token)
  - [Burning a Token](#burning-a-token)
  - [Burning a Non-Fungible Token](#burning-a-non-fungible-token)
  - [Token Update NFTs](#token-update-nfts)
  - [Pausing a Token](#pausing-a-token)
  - [Token Grant KYC](#token-grant-kyc)
  - [Token Revoke KYC](#token-revoke-kyc)
  - [Updating a Token](#updating-a-token)
  - [Cancel Token Airdop](#cancel-token-airdrop)
  - [Querying NFT Info](#querying-nft-info)
  - [Querying Fungible Token Info](#querying-fungible-token-info)
- [HBAR Transactions](#hbar-transactions)
  - [Transferring HBAR](#transferring-hbar)
- [Topic Transactions](#topic-transactions)
  - [Creating a Topic](#creating-a-topic)
  - [Submitting a Topic Message](#submitting-a-topic-message)
  - [Updating a Topic](#updating-a-topic)
  - [Deleting a Topic](#deleting-a-topic)
  - [Querying Topic](#querying-topic)
  - [Querying Topic Message](#querying-topic-message)
- [File Transactions](#file-transactions)
  - [Creating a File](#creating-a-file)
  - [Querying File Info](#querying-file-info)
  - [Querying File Contents](#querying-file-contents)
  - [Updating a File](#updating-a-file)
  - [Deleting a File](#deleting-a-file)
- [Contract Transactions](#contract-transactions)
  - [Creating a Contract](#creating-a-contract)
  - [Querying a Contract Call](#querying-a-contract-call)
  - [Querying Contract Info](#querying-contract-info)
  - [Querying Contract Bytecode](#querying-contract-bytecode)
  - [Updating a Contract](#updating-a-contract)
  - [Executing a Contract](#executing-a-contract)
- [Miscellaneous Queries](#miscellaneous-queries)
  - [Querying Transaction Record](#querying-transaction-record)


## Account Transactions

### Creating an Account

#### Pythonic Syntax:
```
transaction = AccountCreateTransaction(
    key=new_account_public_key,
    initial_balance=initial_balance,
    memo="Test Account"
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)

```
#### Method Chaining:
```
transaction = (
        AccountCreateTransaction()
        .set_key(new_account_public_key)
        .set_initial_balance(initial_balance)
        .set_account_memo("Test")
        .freeze_with(client)
    )
    transaction.sign(client.operator_private_key)
    transaction.execute(client)
```

### Updating an Account

#### Pythonic Syntax:
```python
transaction = AccountUpdateTransaction(
    account_params=AccountUpdateParams(
        account_id=account_id,
        key=new_public_key,
        account_memo=memo,
        receiver_signature_required=receiver_sig_required,
        auto_renew_period=Duration(seconds),
        expiration_time=future_expiration
    )
).freeze_with(client)

transaction.sign(old_private_key)  # Sign with old key
transaction.sign(new_private_key)  # Sign with new key
transaction.execute(client)
```

#### Method Chaining:
```python
transaction = (
    AccountUpdateTransaction()
    .set_account_id(account_id)
    .set_key(new_public_key)
    .set_account_memo(memo)
    .set_receiver_signature_required(receiver_sig_required)
    .set_auto_renew_period(Duration(seconds))
    .set_expiration_time(future_expiration)
    .freeze_with(client)
)
transaction.sign(old_private_key)   # Sign with old key
transaction.sign(new_private_key)   # Sign with new key
transaction.execute(client)
```

### Querying Account Balance

#### Pythonic Syntax:
```
balance = CryptoGetAccountBalanceQuery(account_id=some_account_id).execute(client) print(f"Account balance: {balance.hbars} hbars")
```

#### Method Chaining:
```
balance = ( CryptoGetAccountBalanceQuery() .set_account_id(some_account_id) .execute(client) ) print(f"Account balance: {balance.hbars} hbars")
```

### Querying Account Info

#### Pythonic Syntax:
```
info = AccountInfoQuery(account_id=account_id).execute(client)
print(f"Account ID: {info.account_id}")
print(f"Account Public Key: {info.key.to_string()}")
print(f"Account Balance: {info.balance}")
print(f"Account Memo: '{info.account_memo}'")
print(f"Owned NFTs: {info.owned_nfts}")
print(f"Token Relationships: {info.token_relationships}")
```

#### Method Chaining:
```
info = (
    AccountInfoQuery()
    .set_account_id(account_id)
    .execute(client)
)
print(f"Account ID: {info.account_id}")
print(f"Account Public Key: {info.key.to_string()}")
print(f"Account Balance: {info.balance}")
print(f"Account Memo: '{info.account_memo}'")
print(f"Owned NFTs: {info.owned_nfts}")
print(f"Token Relationships: {info.token_relationships}")
```

## Token Transactions

### Creating a Token

#### Pythonic Syntax:
```
transaction = TokenCreateTransaction(
    token_params=TokenParams(
        token_name="ExampleToken",
        token_symbol="EXT",
        decimals=2,                            # 0 for NON_FUNGIBLE_UNIQUE
        initial_supply=1000,                   # 0 for NON_FUNGIBLE_UNIQUE
        token_type=TokenType.FUNGIBLE_COMMON,  # or TokenType.NON_FUNGIBLE_UNIQUE
        max_supply=1000                        # Must be 0 for INFINITE
        supply_type=SupplyType.FINITE,         # or SupplyType.INFINITE
        freeze_default=False,
        treasury_account_id=operator_id
    ),
    keys=TokenKeys(
        admin_key=admin_key,       # added but optional. Necessary for Token Delete or Update.
        supply_key=supply_key,     # added but optional. Necessary for Token Mint or Burn.
        freeze_key=freeze_key      # added but optional. Necessary to freeze and unfreeze a token.
    )
).freeze_with(client)
transaction.sign(operator_key) # Required signing by the treasury account
transaction.sign(admin_key) # Required since admin key exists
transaction.execute(client)
```

#### Method Chaining:
```
transaction = (
    TokenCreateTransaction()  # no params => uses default placeholders which are next overwritten.
    .set_token_name("ExampleToken")
    .set_token_symbol("EXT")
    .set_decimals(2)                            # 0 for NON_FUNGIBLE_UNIQUE
    .set_initial_supply(1000)                   # 0 for NON_FUNGIBLE_UNIQUE
    .set_token_type(TokenType.FUNGIBLE_COMMON)  # or TokenType.NON_FUNGIBLE_UNIQUE
    .set_max_supply(1000)                       # Must be 0 for INFINITE
    .set_supply_type(SupplyType.FINITE)         # or SupplyType.INFINITE
    .set_freeze_default(False)
    .set_treasury_account_id(operator_id)
    .set_admin_key(admin_key)       # added but optional. Necessary for Token Delete or Update.
    .set_supply_key(supply_key)     # added but optional. Necessary for Token Mint or Burn.
    .set_freeze_key(freeze_key)     # added but optional. Necessary to freeze and unfreeze a token.
    .freeze_with(client)
)

transaction.sign(operator_key) # Required signing by the treasury account
transaction.sign(admin_key)    # Required since admin key exists
transaction.execute(client)
```

### Minting a Fungible Token

#### Pythonic Syntax:
```
transaction = TokenMintTransaction(
    token_id=token_id,
    amount=amount,  # lowest denomination, must be positive and not zero
).freeze_with(client)

transaction.sign(operator_key)
transaction.sign(supply_key)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
    TokenMintTransaction()
    .set_token_id(token_id)
    .set_amount(amount) # lowest denomination, must be positive and not zero
    .freeze_with(client)
)
transaction.sign(operator_key)
transaction.sign(admin_key)
transaction.execute(client)
```

### Minting a Non-Fungible Token

#### Pythonic Syntax:
```
transaction = TokenMintTransaction(
    token_id=token_id,
    metadata=metadata  # Bytes for non-fungible tokens (NFTs)
).freeze_with(client)

transaction.sign(operator_key)
transaction.sign(supply_key)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
    TokenMintTransaction()
    .set_token_id(token_id)
    .set_metadata(metadata)  # Bytes for non-fungible tokens (NFTs)
    .freeze_with(client)
)
transaction.sign(operator_key)
transaction.sign(admin_key)
transaction.execute(client)
```

### Associating a Token

#### Pythonic Syntax:
```
transaction = TokenAssociateTransaction(
    account_id=recipient_id,
    token_ids=[token_id]
).freeze_with(client)

transaction.sign(recipient_key)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
        TokenAssociateTransaction()
        .set_account_id(recipient_id)
        .add_token_id(token_id)
        .freeze_with(client)
        .sign(recipient_key)
    )

    transaction.execute(client)
```

### Dissociating a Token

#### Pythonic Syntax:
```
transaction = TokenDissociateTransaction(
    account_id=recipient_id,
    token_ids=[token_id]
).freeze_with(client)

transaction.sign(recipient_key)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
        TokenDissociateTransaction()
        .set_account_id(recipient_id)
        .add_token_id(token_id)
        .freeze_with(client)
        .sign(recipient_key)
    )

    transaction.execute(client)
```

### Transferring Tokens

#### Pythonic Syntax:
```
transaction = TransferTransaction(
    token_transfers={
        token_id: {
            operator_id: -amount,
            recipient_id: amount
        }
    }
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TransferTransaction()
        .add_token_transfer(token_id, operator_id, -amount)
        .add_token_transfer(token_id, recipient_id, amount)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```

### Transferring NFTs

#### Pythonic Syntax:
```
transaction = TransferTransaction(
    nft_transfers={
        token_id: [
            (
                operator_id,
                recipient_id,
                serial_number
            )
        ]
    }
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TransferTransaction()
        .add_nft_transfer(nft_id, operator_id, recipient_id)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```

### Wiping tokens

#### Pythonic Syntax:
```
transaction = TokenWipeTransaction(
    token_id=token_id,
    account_id=account_id,
    amount=amount
).freeze_with(client)

transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenWipeTransaction()
        .set_token_id(token_id)
        .set_account_id(account_id)
        .set_amount(amount)
        .freeze_with(client)
    )

    transaction.execute(client)
```

### Deleting a Token

#### Pythonic Syntax:
```
transaction = TokenDeleteTransaction(
    token_id=token_id
).freeze_with(client)

transaction.sign(admin_key)  # Admin key must have been set during token creation.
transaction.sign(operator_key)
transaction.execute(client)
```
#### Method Chaining:
```
    transaction = (
        TokenDeleteTransaction()
        .set_token_id(token_id)
        .freeze_with(client)
    )

    transaction.sign(admin_key) # Admin key must also have been set in Token Create
    transaction.sign(operator_key)
    transaction.execute(client)
```

### Freezing a Token

#### Pythonic Syntax:
```
transaction = TokenFreezeTransaction(
    token_id=token_id
    account_id=account_id
).freeze_with(client)

transaction.sign(freeze_key)  # Freeze key must have been set during token creation.
transaction.execute(client)
```
#### Method Chaining:
```
    transaction = (
        TokenFreezeTransaction()
        .set_token_id(token_id)
        .set_account_id(account_id)
        .freeze_with(client)
    )

    transaction.sign(freeze_key) # Freeze key must also have been set in Token Create
    transaction.execute(client)
```
### Unfreezing a Token

#### Pythonic Syntax:
```
transaction = TokenUnfreezeTransaction(
    token_id=token_id
    account_id=account_id
).freeze_with(client)
transaction.sign(freeze_key)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
        TokenUnfreezeTransaction()
        .set_token_id(token_id)
        .set_account_id(account_id)
        .freeze_with(client)
    )
    transaction.sign(freeze_key)
    transaction.execute(client)
```

### Rejecting a Token

#### Pythonic Syntax:
```
transaction = TokenRejectTransaction(
    owner_id=owner_id,
    token_ids=[token_id]
).freeze_with(client)

transaction.sign(owner_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenRejectTransaction()
        .set_owner_id(owner_id)
        .set_token_ids([token_id])
        .freeze_with(client)
        .sign(owner_key)
    )

    transaction.execute(client)
```

### Rejecting a Non-Fungible Token

#### Pythonic Syntax:
```
transaction = TokenRejectTransaction(
    owner_id=owner_id,
    nft_ids=[nft_id1]
).freeze_with(client)

transaction.sign(owner_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenRejectTransaction()
        .set_owner_id(owner_id)
        .set_nft_ids([nft_id1])
        .freeze_with(client)
        .sign(owner_key)
    )

    transaction.execute(client)
```

### Burning a Token

#### Pythonic Syntax:
```
transaction = TokenBurnTransaction(
    token_id=token_id,
    amount=amount
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenBurnTransaction()
        .set_amount(amount)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```

### Burning a Non-Fungible Token

#### Pythonic Syntax:
```
transaction = TokenBurnTransaction(
    token_id=token_id,
    serials=serials
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenBurnTransaction()
        .set_serials(serials)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```

### Token Update NFTs

#### Pythonic Syntax:
```
transaction = TokenUpdateNftsTransaction(
    token_id=nft_token_id,
    serial_numbers=serial_numbers,
    metadata=new_metadata
).freeze_with(client)

transaction.sign(metadata_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenUpdateNftsTransaction()
        .set_token_id(nft_token_id)
        .set_serial_numbers(serial_numbers)
        .set_metadata(new_metadata)
        .freeze_with(client)
        .sign(metadata_key)
    )

    transaction.execute(client)

```

### Pausing a Token

#### Pythonic Syntax:
```
transaction = TokenPauseTransaction(
    token_id=token_id
).freeze_with(client)

transaction.sign(pause_key)
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenPauseTransaction()
        .set_token_id(token_id)
        .freeze_with(client)
        .sign(pause_key)
    )
    transaction.execute(client)

```

### Token Grant KYC

#### Pythonic Syntax:
```
transaction = TokenGrantKycTransaction(
    token_id=token_id,
    account_id=account_id
).freeze_with(client)

transaction.sign(kyc_key)   # KYC key is required for granting KYC approval
transaction.execute(client)

```
#### Method Chaining:
```
    transaction = (
        TokenGrantKycTransaction()
        .set_token_id(token_id)
        .set_account_id(account_id)
        .freeze_with(client)
        .sign(kyc_key)   # KYC key is required for granting KYC approval
    )
    transaction.execute(client)

```

### Updating a Token

#### Pythonic Syntax:
```
transaction = TokenUpdateTransaction(
    token_id=token_id,
    token_params=TokenUpdateParams(
        token_name="UpdateToken",
        token_symbol="UPD",
        token_memo="Updated memo",
        metadata="Updated metadata",
        treasury_account_id=new_account_id
    ),
    token_keys=TokenUpdateKeys(
        admin_key=new_admin_key,
        freeze_key=new_freeze_key, # freeze_key can sign a transaction that changes only the Freeze Key
        metadata_key=new_metadata_key, # metadata_key can sign a transaction that changes only the metadata
        supply_key=new_supply_key   # supply_key can sign a transaction that changes only the Supply Key
    ),
    token_key_verification_mode=TokenKeyValidation.FULL_VALIDATION  # Default value. Also, it can be NO_VALIDATION
).freeze_with(client)
transaction.sign(new_account_id_private_key) # If a new treasury account is set, the new treasury key is required to sign.
transaction.sign(new_admin_key) # Updating the admin key requires the new admin key to sign.
transaction.execute(client)
```

#### Method Chaining:
```
transaction = (
    TokenCreateTransaction()  # no params => uses default placeholders which are next overwritten.
    .set_token_name("UpdateToken")
    .set_token_symbol("UPD")
    .set_token_memo("Updated memo")
    .set_metadata("Updated metadata)
    .set_treasury_account_id(new_account_id)
    .set_admin_key(new_admin_key)
    .set_supply_key(new_supply_key)
    .set_freeze_key(new_freeze_key)
    .set_metadata_key(new_metadata_key)
    .freeze_with(client)
)

transaction.sign(new_account_id_private_key) # If a new treasury account is set, the new treasury key is required to sign.
transaction.sign(new_admin_key) # Updating the admin key requires the new admin key to sign.
transaction.execute(client)
```

### Cancel Token Airdrop

#### Pythonic Syntax:
```
transaction = TokenCancelAirdropTransaction(
    pending_airdrops=pending_airdops  # List of PendingAirdropId
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)
```

#### Method Chaining:
```
transaction = (
    TokenCancelAirdropTransaction()
    .add_pending_airdrop(pending_airdrop) # PendingAirdropId
    .freeze_with(client)
    .sign(operator_key)
)

transaction.execute(client)
```

### Token Revoke KYC

#### Pythonic Syntax:
```
transaction = TokenRevokeKycTransaction(
    token_id=token_id,
    account_id=account_id
).freeze_with(client)

transaction.sign(kyc_key)   # KYC key is required for revoking KYC approval
transaction.execute(client)
```
#### Method Chaining:
```
    transaction = (
        TokenRevokeKycTransaction()
        .set_token_id(token_id)
        .set_account_id(account_id)
        .freeze_with(client)
        .sign(kyc_key)   # KYC key is required for revoking KYC approval
    )

    transaction.execute(client)
```

### Querying NFT Info

#### Pythonic Syntax:
```
nft_info_query = TokenNftInfoQuery(nft_id=nft_id)
nft_info = nft_info_query.execute(client)
print(nft_info)
```
#### Method Chaining:
```
nft_info_query = (
        TokenNftInfoQuery()
        .set_nft_id(nft_id)
    )

nft_info = nft_info_query.execute(client)
print(nft_info)
```

### Querying Fungible Token Info

#### Pythonic Syntax:
```
info_query = TokenInfoQuery(token_id=token_id)
info = info_query.execute(client)
print(info)
```
#### Method Chaining:
```
info_query = (
        TokenInfoQuery()
        .set_token_id(token_id)
    )

info = info_query.execute(client)
print(info)
```

## HBAR Transactions

### Transferring HBAR

#### Pythonic Syntax:
```
transaction = TransferTransaction(
    hbar_transfers={
        operator_id: -100000000,  # send 1 HBAR (in tinybars)
        recipient_id: 100000000
    }
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)
```
#### Method Chaining:
```
    transaction = (
        TransferTransaction()
        .add_hbar_transfer(operator_id, -100000000)  # send 1 HBAR (in tinybars)
        .add_hbar_transfer(recipient_id, 100000000)
        .freeze_with(client)
    )

    transaction.sign(operator_key)
    transaction.execute(client)
```

## Topic Transactions

### Creating a Topic

#### Pythonic Syntax:
```
    transaction = (
        TopicCreateTransaction(
            memo="My Super Topic Memo",
            admin_key=topic_admin_key)
        .freeze_with(client)
        .sign(operator_key)
    )

    transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
    TopicCreateTransaction()
    .set_memo("My Super Topic Memo")
    .set_admin_key(topic_admin_key)
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.execute(client)
```

### Submitting a Topic Message

#### Pythonic Syntax:
```
transaction = (
    TopicMessageSubmitTransaction(topic_id=topic_id, message="Hello, from Python SDK!")
    .freeze_with(client)
    .sign(operator_key)
)

transaction.execute(client)

```
#### Method Chaining:
```
transaction = (
    TopicMessageSubmitTransaction()
    .set_topic_id(topic_id)
    .set_message("Hello, from Python SDK!")
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.execute(client)

```

### Updating a Topic

#### Pythonic Syntax:
```
transaction = (
    TopicUpdateTransaction(topic_id=topic_id, memo="Python SDK updated topic")
    .freeze_with(client)
    .sign(operator_key)
)

transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
    TopicUpdateTransaction()
    .set_topic_id(topic_id)
    .set_memo("Python SDK updated topic")
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.execute(client)

```

### Deleting a Topic

#### Pythonic Syntax:
```
transaction = (
    TopicDeleteTransaction(topic_id=topic_id)
    .freeze_with(client)
    .sign(operator_key)
)
transaction.execute(client)
```
#### Method Chaining:
```
transaction = (
    TopicDeleteTransaction()
    .set_topic_id(topic_id)
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.execute(client)

```

### Querying Topic Info

#### Pythonic Syntax:
```
topic_info_query = TopicInfoQuery(topic_id=topic_id)
topic_info = topic_info_query.execute(client)
print(topic_info)

```
#### Method Chaining:
```
topic_info_query = (
    TopicInfoQuery()
    .set_topic_id(topic_id)
)

topic_info = topic_info_query.execute(client)
print(topic_info)

```

### Querying Topic Message

#### Pythonic Syntax:
```
query = TopicMessageQuery(
    topic_id=topic_id,
    start_time=datetime.now(timezone.utc),
    chunking_enabled=True,
    limit=0
)

query.subscribe(client)

```
#### Method Chaining:
```
query = (
    TopicMessageQuery()
    .set_topic_id(topic_id)
    .set_start_time(datetime.now(timezone.utc))
    .set_chunking_enabled(True)
    .set_limit(0)
    )

query.subscribe(client)
```

## File Transactions

### Creating a File

#### Pythonic Syntax:
```
transaction = FileCreateTransaction(
    keys=[account_public_key],
    contents=file_contents,
    file_memo="My first file on Hedera"
).freeze_with(client)

transaction.sign(account_private_key)
transaction.execute(client)
```

#### Method Chaining:
```
    transaction = (
        FileCreateTransaction()
        .set_keys(account_public_key)
        .set_contents(file_contents)
        .set_file_memo("My first file on Hedera")
        .freeze_with(client)
        .sign(account_private_key)
    )

    transaction.execute(client)

```

### Querying File Info

#### Pythonic Syntax:
```
file_info_query = FileInfoQuery(file_id=file_id)
file_info = file_info_query.execute(client)
print(file_info)
```

#### Method Chaining:
```
file_info = (
    FileInfoQuery()
    .set_file_id(file_id)
    .execute(client)
)
print(file_info)

```

### Querying File Contents

#### Pythonic Syntax:
```
file_contents_query = FileContentsQuery(file_id=file_id)
file_contents = file_contents_query.execute(client)
print(str(file_contents)) # decode bytes to string
```

#### Method Chaining:
```
file_contents = (
    FileContentsQuery()
    .set_file_id(file_id)
    .execute(client)
)
print(str(file_contents)) # decode bytes to string

```

### Updating a File

#### Pythonic Syntax:
```
transaction = FileUpdateTransaction(
    file_id=file_id,
    keys=[new_file_public_key],
    contents=b"New File Contents",
    file_memo="Updated file memo"
).freeze_with(client)

transaction.sign(current_file_private_key)
transaction.sign(new_file_private_key)
transaction.execute(client)
```

#### Method Chaining:
```
    transaction = (
        FileUpdateTransaction()
        .set_file_id(file_id)
        .set_keys([new_file_public_key])
        .set_contents(b"New File Contents")
        .set_file_memo("Updated file memo")
        .freeze_with(client)
        .sign(current_file_private_key)
        .sign(new_file_private_key)
    )

    transaction.execute(client)

```

### Deleting a File

#### Pythonic Syntax:
```
transaction = FileDeleteTransaction(
    file_id=file_id
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)
```

#### Method Chaining:
```
    transaction = (
        FileDeleteTransaction()
        .set_file_id(file_id)
        .freeze_with(client)
    )

    transaction.sign(operator_key)
    transaction.execute(client)

```


## Contract Transactions

### Creating a Contract

#### Pythonic Syntax:
```
# First, create a file with the contract bytecode
transaction = FileCreateTransaction(
    keys=[operator_key.public_key()],
    contents=contract_bytecode,
    file_memo="Contract bytecode file"
).freeze_with(client)

transaction.sign(operator_key)
file_receipt = transaction.execute(client)

file_id = file_receipt.file_id

# Create constructor parameters if needed
constructor_params = ContractFunctionParameters().add_string("Hello, World!")

# Create the contract using bytecode from file
transaction = ContractCreateTransaction(
    contract_params=ContractCreateParams(
        bytecode_file_id=file_id,
        gas=200000,
        admin_key=admin_key,
        initial_balance=100000000,  # 1 HBAR in tinybars
        parameters=constructor_params.to_bytes(),
        contract_memo="My first smart contract"
    )
).freeze_with(client)

transaction.sign(operator_key)
transaction.sign(admin_key)
transaction.execute(client)
```

#### Method Chaining:
```
# First, create a file with the contract bytecode
file_receipt = (
    FileCreateTransaction()
    .set_keys(operator_key.public_key())
    .set_contents(contract_bytecode)
    .set_file_memo("Contract bytecode file")
    .freeze_with(client)
    .sign(operator_key)
    .execute(client)
)

file_id = file_receipt.file_id

# Create constructor parameters if needed
constructor_params = ContractFunctionParameters().add_string("Hello, World!")

# Create the contract using bytecode from file
transaction = (
    ContractCreateTransaction()
    .set_bytecode_file_id(file_id)
    .set_gas(200000)
    .set_admin_key(admin_key)
    .set_initial_balance(100000000)  # 1 HBAR in tinybars
    .set_constructor_parameters(constructor_params)
    .set_contract_memo("My first smart contract")
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.sign(admin_key)
transaction.execute(client)
```

#### Creating a Contract with Direct Bytecode:
```
##### Convert hex bytecode to bytes
bytecode = bytes.fromhex(contract_bytecode_hex)

# Create constructor parameters if needed
constructor_params = ContractFunctionParameters().add_string("Hello, World!")

# Create the contract using bytecode directly
transaction = (
    ContractCreateTransaction()
    .set_bytecode(bytecode)
    .set_gas(200000)
    .set_admin_key(admin_key)
    .set_initial_balance(100000000)  # 1 HBAR in tinybars
    .set_constructor_parameters(constructor_params)
    .set_contract_memo("My first smart contract")
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.sign(admin_key)
transaction.execute(client)
```

### Querying a Contract Call

#### Pythonic Syntax:
```
# Query a contract function that returns value(s)
# Example: calling getMessageAndOwner() (StatefulContract.sol) which returns (bytes32 message, address owner)
result = ContractCallQuery(
    contract_id=contract_id,
    gas=2000000,
    function_parameters=ContractFunctionParameters("getMessageAndOwner").to_bytes()  # Function name to call
).execute(client)

# Extract return values by their position in the Solidity return statement
# getMessageAndOwner() returns (bytes32, address), so:
# - index 0: bytes32 message
# - index 1: address owner
message = result.get_bytes32(0)
owner_address = result.get_address(1)

print(f"Message: {message}")
print(f"Owner: {owner_address}")

# Alternative way using get_result with type specifications
result_values = result.get_result(["bytes32", "address"])
print(f"Message: {result_values[0]}")
print(f"Owner: {result_values[1]}")
```

#### Method Chaining:
```
# Query a contract function using method chaining
# Example: calling getMessageAndOwner() (StatefulContract.sol) which returns (bytes32 message, address owner)
result = (
    ContractCallQuery()
    .set_contract_id(contract_id)
    .set_gas(2000000)
    .set_function("getMessageAndOwner")  # Function name to call
    .execute(client)
)

# Alternatively, you can use set_function_parameters() with ContractFunctionParameters:
result = (
    ContractCallQuery()
    .set_contract_id(contract_id)
    .set_gas(2000000)
    .set_function_parameters(ContractFunctionParameters("getMessageAndOwner"))
    .execute(client)
)


# Extract return values by their position in the Solidity return statement
# getMessageAndOwner() returns (bytes32, address), so:
# - index 0: bytes32 message
# - index 1: address owner
message = result.get_bytes32(0)
owner_address = result.get_address(1)

print(f"Message: {message}")
print(f"Owner: {owner_address}")

# Alternative way using get_result with type specifications
result_values = result.get_result(["bytes32", "address"])
print(f"Message: {result_values[0]}")
print(f"Owner: {result_values[1]}")

# For different Solidity return types, use these methods:
#
# String values:     result.get_string(0)
# Address values:    result.get_address(1)
# Number values:     result.get_uint256(2)
# Boolean values:    result.get_bool(3)
# Bytes32 values:    result.get_bytes32(4)
# Bytes values:      result.get_bytes(5)
#
# Note: The index number matches the position in your Solidity return statement
# Example: function getData() returns (string, address, uint256, bool)
# - result.get_string(0)    // first return value
# - result.get_address(1)   // second return value
# - result.get_uint256(2)   // third return value
# - result.get_bool(3)      // fourth return value
```

### Querying Contract Info

#### Pythonic Syntax:
```
contract_info_query = ContractInfoQuery(contract_id=contract_id)
contract_info = contract_info_query.execute(client)
print(contract_info)
```

#### Method Chaining:
```
contract_info = (
    ContractInfoQuery()
    .set_contract_id(contract_id)
    .execute(client)
)
print(contract_info)
```

### Querying Contract Bytecode

#### Pythonic Syntax:
```
contract_bytecode_query = ContractBytecodeQuery(contract_id=contract_id)
contract_bytecode = contract_bytecode_query.execute(client)
print(contract_bytecode.hex()) # display bytecode as hex string
```

#### Method Chaining:
```
contract_bytecode = (
    ContractBytecodeQuery()
    .set_contract_id(contract_id)
    .execute(client)
)
print(contract_bytecode.hex()) # display bytecode as hex string
```

### Updating a Contract

#### Pythonic Syntax:
```python
transaction = ContractUpdateTransaction(
    contract_params=ContractUpdateParams(
        contract_id=contract_id,
        admin_key=new_admin_key,
        contract_memo="Updated contract memo",
        expiration_time=new_expiration_time,
        auto_renew_period=Duration(seconds),
        auto_renew_account_id=new_auto_renew_account,
        max_automatic_token_associations=100,
    )
).freeze_with(client)

transaction.sign(current_admin_key)  # Sign with current admin key
transaction.sign(new_admin_key)      # Sign with new admin key
transaction.execute(client)
```

#### Method Chaining:
```python
transaction = (
    ContractUpdateTransaction()
    .set_contract_id(contract_id)
    .set_admin_key(new_admin_key)
    .set_contract_memo("Updated contract memo")
    .set_expiration_time(new_expiration_time)
    .set_auto_renew_period(Duration(seconds))
    .set_auto_renew_account_id(new_auto_renew_account)
    .set_max_automatic_token_associations(100)
    .freeze_with(client)
)

transaction.sign(current_admin_key)  # Sign with current admin key
transaction.sign(new_admin_key)      # Sign with new admin key
transaction.execute(client)
```

### Executing a Contract

#### Pythonic Syntax:
```python
# Example: calling setMessage(bytes32) (StatefulContract.sol)
# Prepare function parameters for setMessage(bytes32)
func_params = ContractFunctionParameters("setMessage").add_bytes32(b"New message")

transaction = ContractExecuteTransaction(
    contract_id=contract_id,
    gas=1000000,
    function_parameters=func_params.to_bytes() # function to execute
).freeze_with(client)

transaction.sign(operator_key)
transaction.execute(client)
```

#### Method Chaining:
```python
# Execute a contract function using method chaining
# Example: calling setMessage(bytes32) (StatefulContract.sol)
transaction = (
    ContractExecuteTransaction()
    .set_contract_id(contract_id)
    .set_gas(1000000)
    .set_function("setMessage",ContractFunctionParameters().add_bytes32(b"New message"))
    .freeze_with(client)
)

# Alternatively, you can use set_function_parameters() with ContractFunctionParameters:
transaction = (
    ContractExecuteTransaction()
    .set_contract_id(contract_id)
    .set_gas(1000000)
    .set_function(ContractFunctionParameters("setMessage").add_bytes32(b"New message"))
    .freeze_with(client)
)

transaction.sign(operator_key)
transaction.execute(client)
```


## Miscellaneous Queries

### Querying Transaction Record

#### Pythonic Syntax:
```
query = TransactionRecordQuery(
    transaction_id=transaction_id
)

record = query.execute(client)

print(f"Transaction ID: {record.transaction_id}")
print(f"Transaction Fee: {record.transaction_fee}")
print(f"Transaction Hash: {record.transaction_hash}")
print(f"Transaction Memo: {record.transaction_memo}")
print(f"Transaction Account ID: {record.receipt.account_id}")
```
#### Method Chaining:
```
record = (
    TransactionRecordQuery()
    .set_transaction_id(transaction_id)
    .execute(client)
)

print(f"Transaction ID: {record.transaction_id}")
print(f"Transaction Fee: {record.transaction_fee}")
print(f"Transaction Hash: {record.transaction_hash}")
print(f"Transaction Memo: {record.transaction_memo}")
print(f"Transaction Account ID: {record.receipt.account_id}")
```
