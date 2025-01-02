from hedera_sdk_python.transaction.transaction import Transaction
from hedera_sdk_python.hapi.services import crypto_create_pb2, duration_pb2
from hedera_sdk_python.response_code import ResponseCode
from hedera_sdk_python.crypto.public_key import PublicKey
from hedera_sdk_python.hbar import Hbar


class AccountCreateTransaction(Transaction):
    """
    Represents an account creation transaction on the Hedera network.
    """

    def __init__(self, key=None, initial_balance=0, receiver_signature_required=False, auto_renew_period=7890000, memo=""):
        """
        Initializes a new AccountCreateTransaction instance with default values or keyword arguments.

        Args:
            key (PublicKey, optional): The public key for the new account.
            initial_balance (int or Hbar, optional): Initial balance in tinybars or as an Hbar instance.
            receiver_signature_required (bool, optional): Whether receiver signature is required.
            auto_renew_period (int, optional): Auto-renew period in seconds (default is 90 days).
            memo (str, optional): Memo for the account.
        """
        super().__init__()
        self.key = key
        self.initial_balance = initial_balance
        self.receiver_signature_required = receiver_signature_required
        self.auto_renew_period = auto_renew_period
        self.account_memo = memo

        self._default_transaction_fee = 300_000_000

    def set_initial_balance(self, balance):
        self._require_not_frozen()
        if not isinstance(balance, (Hbar, int)):
            raise TypeError("initial_balance must be an instance of Hbar or int representing tinybars.")
        self.initial_balance = balance
        return self

    def set_key(self, key: PublicKey):
        self._require_not_frozen()
        self.key = key
        return self

    def set_receiver_signature_required(self, required: bool):
        self._require_not_frozen()
        self.receiver_signature_required = required
        return self

    def set_auto_renew_period(self, seconds: int):
        self._require_not_frozen()
        self.auto_renew_period = seconds
        return self

    def set_account_memo(self, memo: str):
        self._require_not_frozen()
        self.account_memo = memo
        return self

    def build_transaction_body(self):
        """
        Builds and returns the protobuf transaction body for account creation.

        Returns:
            TransactionBody: The protobuf transaction body containing the account creation details.

        Raises:
            ValueError: If required fields are missing.
        """
        if not self.key:
            raise ValueError("Key must be set.")
        
        if self.initial_balance is None:
            initial_balance_tinybars = 0
        elif isinstance(self.initial_balance, Hbar):
            initial_balance_tinybars = self.initial_balance.to_tinybars()
        elif isinstance(self.initial_balance, int):
            initial_balance_tinybars = self.initial_balance
        else:
            raise TypeError("initial_balance must be an instance of Hbar or int representing tinybars.")

        crypto_create_body = crypto_create_pb2.CryptoCreateTransactionBody(
            key=self.key.to_proto(),
            initialBalance=initial_balance_tinybars,
            receiverSigRequired=self.receiver_signature_required,
            autoRenewPeriod=duration_pb2.Duration(seconds=self.auto_renew_period),
            memo=self.account_memo
        )

        transaction_body = self.build_base_transaction_body()
        transaction_body.cryptoCreateAccount.CopyFrom(crypto_create_body)

        return transaction_body

    def _execute_transaction(self, client, transaction_proto):
        """
        Executes the account creation transaction using the provided client.

        Args:
            client (Client): The client instance to use for execution.
            transaction_proto (Transaction): The protobuf Transaction message.

        Returns:
            TransactionReceipt: The receipt from the network after transaction execution.

        Raises:
            Exception: If the transaction submission fails or receives an error response.
        """
        response = client.crypto_stub.createAccount(transaction_proto)

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
            timeout (int): Maximum time in seconds to wait for the receipt.

        Returns:
            TransactionReceipt: The transaction receipt from the network.

        Raises:
            Exception: If the transaction ID is not set or if receipt retrieval fails.
        """
        if self.transaction_id is None:
            raise Exception("Transaction ID is not set.")

        receipt = client.get_transaction_receipt(self.transaction_id, timeout)
        return receipt