from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

class PrivateKey:
    def __init__(self, private_key):
        self._private_key = private_key

    @classmethod
    def from_string(cls, key_str):
        key_bytes = bytes.fromhex(key_str)
        try:
            private_key = serialization.load_der_private_key(
                data=key_bytes,
                password=None
            )
        except Exception as e:
            print(f"Error loading DER private key: {e}")
            raise
        return cls(private_key)

    def sign(self, data):
        return self._private_key.sign(data)

    def public_key(self):
        return self._private_key.public_key()
