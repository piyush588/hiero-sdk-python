from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class PrivateKey:
    def __init__(self, private_key):
        self._private_key = private_key

    @classmethod
    def from_string(cls, key_str):
        """
        Load a private key from a hex-encoded string. Supports both raw private keys (32 bytes)
        and DER-encoded private keys.
        """
        try:
            key_bytes = bytes.fromhex(key_str)
        except ValueError:
            raise ValueError("Invalid hex-encoded private key string.")

        try:
            if len(key_bytes) == 32:
                private_key = ed25519.Ed25519PrivateKey.from_private_bytes(key_bytes)
            else:
                private_key = serialization.load_der_private_key(
                    key_bytes, password=None
                )
                if not isinstance(private_key, ed25519.Ed25519PrivateKey):
                    raise TypeError("The key is not an Ed25519 private key.")
            return cls(private_key)
        except Exception as e:
            print(f"Error loading Ed25519 private key: {e}")
            raise ValueError("Failed to load private key.")

    def sign(self, data):
        return self._private_key.sign(data)

    def public_key(self):
        return self._private_key.public_key()