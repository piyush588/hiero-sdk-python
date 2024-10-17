from src.transaction.transaction import Transaction
from src.outputs import crypto_transfer_pb2, basic_types_pb2
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from collections import defaultdict
from src.transaction.transaction_receipt import TransactionReceipt
from src.response_code import ResponseCode

class TransferTransaction(Transaction):
    """
    Represents a transaction to transfer HBAR or tokens between accounts.
    """

    def __init__(self):
        super().__init__()
        self.hbar_transfers = defaultdict(int)
        self.token_transfers = defaultdict(lambda: defaultdict(int))

        self._default_transaction_fee = 100_000_000

    def add_hbar_transfer(self, account_id: AccountId, amount: int) -> 'TransferTransaction':
        """
        Adds a HBAR transfer to the transaction.

        Args:
            account_id (AccountId): The account ID.
            amount (int): The amount to transfer (positive or negative).

        Returns:
            TransferTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(account_id, AccountId):
            raise TypeError("account_id must be an AccountId instance.")
        if not isinstance(amount, int) or amount == 0:
            raise ValueError("Amount must be a non-zero integer.")

        self.hbar_transfers[account_id] += amount
        return self

    def add_token_transfer(self, token_id: TokenId, account_id: AccountId, amount: int) -> 'TransferTransaction':
        """
        Adds a token transfer to the transaction.

        Args:
            token_id (TokenId): The token ID.
            account_id (AccountId): The account ID.
            amount (int): The amount to transfer (positive or negative).

        Returns:
            TransferTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(token_id, TokenId):
            raise TypeError("token_id must be a TokenId instance.")
        if not isinstance(account_id, AccountId):
            raise TypeError("account_id must be an AccountId instance.")
        if not isinstance(amount, int) or amount == 0:
            raise ValueError("Amount must be a non-zero integer.")

        self.token_transfers[token_id][account_id] += amount
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for a transfer transaction.

        Returns:
            TransactionBody: The protobuf transaction body.
        """
        crypto_transfer_tx_body = crypto_transfer_pb2.CryptoTransferTransactionBody()

        # HBAR 
        if self.hbar_transfers:
            transfer_list = basic_types_pb2.TransferList()
            for account_id, amount in self.hbar_transfers.items():
                account_amount = basic_types_pb2.AccountAmount()
                account_amount.accountID.CopyFrom(account_id.to_proto())
                account_amount.amount = amount
                transfer_list.accountAmounts.append(account_amount)
            crypto_transfer_tx_body.transfers.CopyFrom(transfer_list)

        # Token 
        for token_id, transfers in self.token_transfers.items():
            token_transfer_list = basic_types_pb2.TokenTransferList()
            token_transfer_list.token.CopyFrom(token_id.to_proto())
            for account_id, amount in transfers.items():
                account_amount = basic_types_pb2.AccountAmount()
                account_amount.accountID.CopyFrom(account_id.to_proto())
                account_amount.amount = amount
                token_transfer_list.transfers.append(account_amount)
            crypto_transfer_tx_body.tokenTransfers.append(token_transfer_list)

        return self.build_base_transaction_body(crypto_transfer_tx_body)

    def freeze_with(self, client):
        """
        Freezes the transaction with the provided client.

        Args:
            client (Client): The client instance.

        Returns:
            TransferTransaction: The instance for chaining.
        """
        self.client = client
        if self.transaction_id is None:
            self.transaction_id = client.generate_transaction_id()

        if self.node_account_id is None:
            self.node_account_id = client.network.node_account_id

        self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        return self

    def execute(self, client=None):
        """
        Executes the transaction using the provided client.

        Args:
            client (Client): The client instance. If None, uses the client from freeze_with.

        Returns:
            TransactionReceipt: The receipt from the network.
        """
        if client is None:
            client = self.client
        if client is None:
            raise ValueError("Client must be provided either in freeze_with or execute.")

        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be frozen before execution. Call freeze_with(client) first.")

        if not self.is_signed_by(client.operator_private_key.public_key()):
            self.sign(client.operator_private_key)

        transaction_proto = self.to_proto()
        response = client.crypto_stub.cryptoTransfer(transaction_proto)

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        receipt = self.get_receipt(client)
        return receipt

    def get_receipt(self, client, timeout=60):
        """
        Retrieves the receipt for the transaction.

        Args:
            client (Client): The client instance.
            timeout (int): Timeout in seconds.

        Returns:
            TransactionReceipt: The transaction receipt.
        """
        if self.transaction_id is None:
            raise Exception("Transaction ID is not set.")

        receipt = client.get_transaction_receipt(self.transaction_id, timeout)
        return receipt
