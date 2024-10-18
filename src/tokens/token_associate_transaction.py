from src.transaction.transaction import Transaction
from src.outputs import token_associate_pb2
from src.account.account_id import AccountId
from src.tokens.token_id import TokenId
from typing import List
from src.response_code import ResponseCode

class TokenAssociateTransaction(Transaction):
    """
    Represents a transaction to associate tokens with an account.
    """

    def __init__(self):
        super().__init__()
        self.account_id = None
        self.token_ids = []

        self._default_transaction_fee = 500_000_000

    def set_account_id(self, account_id: AccountId) -> 'TokenAssociateTransaction':
        """
        Sets the account ID to associate tokens with.

        Args:
            account_id (AccountId): The account ID.

        Returns:
            TokenAssociateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(account_id, AccountId):
            raise TypeError("Account ID must be an AccountId instance.")
        self.account_id = account_id
        return self

    def add_token_id(self, token_id: TokenId) -> 'TokenAssociateTransaction':
        """
        Adds a token ID to associate with the account.

        Args:
            token_id (TokenId): The token ID to associate.

        Returns:
            TokenAssociateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(token_id, TokenId):
            raise TypeError("Token ID must be a TokenId instance.")
        self.token_ids.append(token_id)
        return self

    def set_token_ids(self, token_ids: List[TokenId]) -> 'TokenAssociateTransaction':
        """
        Sets the list of token IDs to associate with the account.

        Args:
            token_ids (List[TokenId]): A list of token IDs.

        Returns:
            TokenAssociateTransaction: The instance of the transaction for chaining.
        """
        if not all(isinstance(token_id, TokenId) for token_id in token_ids):
            raise TypeError("All token IDs must be TokenId instances.")
        self.token_ids = token_ids
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for token association.

        Returns:
            TransactionBody: The protobuf transaction body.
        """
        if not self.account_id or not self.token_ids:
            raise ValueError("Account ID and token IDs must be set.")

        token_associate_tx_body = token_associate_pb2.TokenAssociateTransactionBody()
        token_associate_tx_body.account.CopyFrom(self.account_id.to_proto())
        token_associate_tx_body.tokens.extend([token_id.to_proto() for token_id in self.token_ids])

        return self.build_base_transaction_body(token_associate_tx_body)

    def freeze_with(self, client):
        """
        Freezes the transaction with the provided client.

        Args:
            client (Client): The client instance.

        Returns:
            TokenAssociateTransaction: The instance for chaining.
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

        Raises:
            ValueError: If the client is not provided.
            Exception: If the transaction submission fails.
        """
        if client is None:
            client = self.client
        if client is None:
            raise ValueError("Client must be provided either in freeze_with or execute.")

        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be frozen before execution. Call freeze_with(client) first.")

        transaction_proto = self.to_proto()

        response = client.token_stub.associateTokens(transaction_proto)

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
