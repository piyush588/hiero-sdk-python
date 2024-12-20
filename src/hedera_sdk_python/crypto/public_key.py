from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class PublicKey:
    def __init__(self, public_key):
        self._public_key = public_key

    def verify(self, signature, data):
        """
        Verifies a signature for the given data using the public key.

        Args:
            signature (bytes): The signature to verify.
            data (bytes): The data that was signed.

        Raises:
            cryptography.exceptions.InvalidSignature: If the signature is invalid.
        """
        self._public_key.verify(signature, data)

    def to_string(self):
        """
        Returns the public key as a hex-encoded string.

        Returns:
            str: The hex-encoded public key.
        """
        public_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return public_bytes.hex()

    def to_proto(self):
        """
        Returns the protobuf representation of the public key.

        Returns:
            Key: The protobuf Key message.
        """
        from hedera_sdk_python.hapi import basic_types_pb2
        public_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        return basic_types_pb2.Key(ed25519=public_bytes)

    def public_bytes(self, encoding, format):
        """
        Returns the public key bytes in the specified encoding and format.

        Args:
            encoding (Encoding): The encoding to use.
            format (PublicFormat): The public key format.

        Returns:
            bytes: The public key bytes.
        """
        return self._public_key.public_bytes(encoding=encoding, format=format)
