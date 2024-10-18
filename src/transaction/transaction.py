from src.outputs import (
    transaction_pb2, transaction_body_pb2, basic_types_pb2,
    transaction_contents_pb2, token_create_pb2, token_associate_pb2, crypto_transfer_pb2
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

class Transaction:
    def __init__(self):
        self.transaction_id = None
        self.node_account_id = None
        self.transaction_fee = None
        self.transaction_valid_duration = 120
        self.generate_record = False
        self.memo = ""
        self.transaction_body_bytes = None
        self.signature_map = basic_types_pb2.SignatureMap()

        self._default_transaction_fee = 2_000_000

    def sign(self, private_key):
        """
        Sign the transaction using the provided private key.
        """
        if self.transaction_body_bytes is None:
            self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        signature = private_key.sign(self.transaction_body_bytes)

        public_key_bytes = private_key.public_key().public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )

        sig_pair = basic_types_pb2.SignaturePair(
            pubKeyPrefix=public_key_bytes[:6],
            ed25519=signature
        )

        self.signature_map.sigPair.append(sig_pair)

        return self

    def to_proto(self):
        """
        Serialize the signed transaction into a protobuf message.
        """
        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be signed before calling to_proto()")

        signed_transaction = transaction_contents_pb2.SignedTransaction(
            bodyBytes=self.transaction_body_bytes,
            sigMap=self.signature_map
        )

        return transaction_pb2.Transaction(
            signedTransactionBytes=signed_transaction.SerializeToString()
        )

    def setup_base_transaction(self, transaction_id=None, node_account_id=None, transaction_fee=None, memo=None):
        """
        Common function to set up the base transaction fields.
        """
        self.transaction_id = transaction_id or self.transaction_id
        self.node_account_id = node_account_id or self.node_account_id
        if transaction_fee is not None:
            self.transaction_fee = transaction_fee
        if memo is not None:
            self.memo = memo

    def build_base_transaction_body(self, specific_tx_body):
        """
        Builds the base transaction body by combining the base transaction fields
        with the specific transaction body fields (e.g., token associate, transfer).
        """
        transaction_body = transaction_body_pb2.TransactionBody()

        if not self.transaction_id:
            raise ValueError("Transaction ID must be set before building the transaction body.")
        if not self.node_account_id:
            raise ValueError("Node account ID must be set before building the transaction body.")

        transaction_body.transactionID.CopyFrom(self.transaction_id)
        transaction_body.nodeAccountID.CopyFrom(self.node_account_id.to_proto())
        transaction_body.transactionFee = self.transaction_fee or self._default_transaction_fee
        transaction_body.transactionValidDuration.seconds = self.transaction_valid_duration
        transaction_body.generateRecord = self.generate_record
        transaction_body.memo = self.memo

        # set specific transaction body (like token associate, transfer, etc.)
        if isinstance(specific_tx_body, token_create_pb2.TokenCreateTransactionBody):
            transaction_body.tokenCreation.CopyFrom(specific_tx_body)
        elif isinstance(specific_tx_body, token_associate_pb2.TokenAssociateTransactionBody):
            transaction_body.tokenAssociate.CopyFrom(specific_tx_body)
        elif isinstance(specific_tx_body, crypto_transfer_pb2.CryptoTransferTransactionBody):
            transaction_body.cryptoTransfer.CopyFrom(specific_tx_body)
        else:
            raise ValueError("Unsupported transaction type")

        return transaction_body

    def freeze_with(self, client):
        """
        Freezes the transaction with the provided client.

        Args:
            client (Client): The client instance.

        Returns:
            Transaction: The instance for chaining.
        """
        if self.transaction_id is None:
            self.transaction_id = client.generate_transaction_id()

        if self.node_account_id is None:
            self.node_account_id = client.network.node_account_id

        self.transaction_body_bytes = self.build_transaction_body().SerializeToString()

        return self

    def execute(self, client):
        """
        Executes the transaction using the provided client.

        Args:
            client (Client): The client instance.

        Returns:
            TransactionResponse: The response from the network.
        """
        if self.transaction_body_bytes is None:
            raise Exception("Transaction must be frozen before execution. Call freeze_with(client) first.")

        if not self.is_signed_by(client.operator_private_key.public_key()):
            self.sign(client.operator_private_key)

        transaction_proto = self.to_proto()

        response = self.execute_transaction(client, transaction_proto)

        return response

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

    def is_signed_by(self, public_key):
        """
        Checks if the transaction has been signed by the given public key.

        Args:
            public_key: The public key to check.

        Returns:
            bool: True if signed by the public key, False otherwise.
        """
        public_key_bytes = public_key.public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )
        pub_key_prefix = public_key_bytes[:6]

        for sig_pair in self.signature_map.sigPair:
            if sig_pair.pubKeyPrefix == pub_key_prefix:
                return True
        return False

    def build_transaction_body(self):
        """
        Abstract method to build the transaction body.
        Should be implemented by subclasses.

        Returns:
            TransactionBody: The protobuf TransactionBody message.
        """
        raise NotImplementedError("Subclasses must implement build_transaction_body()")

    def execute_transaction(self, client, transaction_proto):
        """
        Abstract method to execute the transaction.
        Should be implemented by subclasses.

        Args:
            client (Client): The client instance.
            transaction_proto (Transaction): The transaction protobuf message.

        Returns:
            Response: The response from the network.
        """
        raise NotImplementedError("Subclasses must implement execute_transaction()")
