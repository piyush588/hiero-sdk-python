from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class PrivateKey:
    def __init__(self, private_key):
        self._private_key = private_key  # Ed25519

    @classmethod
    def from_string(cls, key_str):
        key_bytes = bytes.fromhex(key_str)
        private_key = serialization.load_der_private_key(
            key_bytes,
            password=None,
            backend=default_backend()
        )
        return cls(private_key)

    def sign(self, message):
        return self._private_key.sign(message)

    def public_key(self):
        return self._private_key.public_key()
