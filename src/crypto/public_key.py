class PublicKey:
    def __init__(self, key):
        self._key = key

    def to_bytes(self):
        return self._key.public_bytes()
