# token_create_transaction.py

from src.transaction.transaction import Transaction
from src.outputs import token_create_pb2
from src.account.account_id import AccountId
from src.response_code import ResponseCode

class TokenCreateTransaction(Transaction):
    """
    Represents a transaction to create a new token on the Hedera network.
    """

    def __init__(self):
        super().__init__()
        self.token_name = None
        self.token_symbol = None
        self.decimals = None
        self.initial_supply = None
        self.treasury_account_id = None

        self._default_transaction_fee = 3_000_000_000

    def set_token_name(self, name: str) -> 'TokenCreateTransaction':
        """
        Sets the name of the token.

        Args:
            name (str): The name of the token.

        Returns:
            TokenCreateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(name, str):
            raise TypeError("Token name must be a string.")
        self.token_name = name
        return self

    def set_token_symbol(self, symbol: str) -> 'TokenCreateTransaction':
        """
        Sets the symbol of the token.

        Args:
            symbol (str): The symbol of the token.

        Returns:
            TokenCreateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(symbol, str):
            raise TypeError("Token symbol must be a string.")
        self.token_symbol = symbol
        return self

    def set_decimals(self, decimals: int) -> 'TokenCreateTransaction':
        """
        Sets the number of decimal places the token supports.

        Args:
            decimals (int): The number of decimals.

        Returns:
            TokenCreateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(decimals, int) or decimals < 0:
            raise ValueError("Decimals must be a non-negative integer.")
        self.decimals = decimals
        return self

    def set_initial_supply(self, supply: int) -> 'TokenCreateTransaction':
        """
        Sets the initial supply of the token.

        Args:
            supply (int): The initial supply.

        Returns:
            TokenCreateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(supply, int) or supply < 0:
            raise ValueError("Initial supply must be a non-negative integer.")
        self.initial_supply = supply
        return self

    def set_treasury_account_id(self, account_id: AccountId) -> 'TokenCreateTransaction':
        """
        Sets the treasury account ID for the token.

        Args:
            account_id (AccountId): The treasury account ID.

        Returns:
            TokenCreateTransaction: The instance of the transaction for chaining.
        """
        if not isinstance(account_id, AccountId):
            raise TypeError("Treasury account ID must be an AccountId instance.")
        self.treasury_account_id = account_id
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for token creation.

        Returns:
            TransactionBody: The protobuf transaction body.
        """
        required_fields = [
            ('token_name', self.token_name),
            ('token_symbol', self.token_symbol),
            ('decimals', self.decimals),
            ('initial_supply', self.initial_supply),
            ('treasury_account_id', self.treasury_account_id),
        ]

        missing_fields = [name for name, value in required_fields if value is None]
        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            raise ValueError(f"Missing required fields: {missing_fields_str}")

        token_create_tx_body = token_create_pb2.TokenCreateTransactionBody()
        token_create_tx_body.name = self.token_name
        token_create_tx_body.symbol = self.token_symbol
        token_create_tx_body.decimals = self.decimals
        token_create_tx_body.initialSupply = self.initial_supply
        token_create_tx_body.treasury.CopyFrom(self.treasury_account_id.to_proto())

        return self.build_base_transaction_body(token_create_tx_body)

    def freeze_with(self, client):
        """
        Freezes the transaction with the provided client.

        Args:
            client (Client): The client instance.

        Returns:
            TokenCreateTransaction: The instance for chaining.
        """
        self.client = client
        if self.transaction_id is None:
            # Generate transaction ID using the client's operator account ID
            self.transaction_id = client.generate_transaction_id()

        if self.node_account_id is None:
            # Use the client's node account ID
            self.node_account_id = client.network.node_account_id

        # Build the transaction body bytes
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

        # Sign the transaction with the client's operator private key if not already signed
        if not self.is_signed_by(client.operator_private_key.public_key()):
            self.sign(client.operator_private_key)

        # Build the transaction protobuf message
        transaction_proto = self.to_proto()

        # Submit the transaction using the client's token stub
        response = client.token_stub.createToken(transaction_proto)

        if response.nodeTransactionPrecheckCode != ResponseCode.OK:
            error_code = response.nodeTransactionPrecheckCode
            error_message = ResponseCode.get_name(error_code)
            raise Exception(f"Error during transaction submission: {error_code} ({error_message})")

        # Wait for receipt
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

        # Use the client's method to get the transaction receipt
        receipt = client.get_transaction_receipt(self.transaction_id, timeout)
        return receipt
