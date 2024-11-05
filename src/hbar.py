class Hbar:

    TINYBAR_TO_HBAR = 100_000_000

    def __init__(self, amount, in_tinybars=False):
        if in_tinybars:
            self._amount_in_tinybar = int(amount)
        else:
            self._amount_in_tinybar = int(amount * self.TINYBAR_TO_HBAR)

    def to_tinybars(self):
        return self._amount_in_tinybar

    def to_hbars(self):
        return self._amount_in_tinybar / self.TINYBAR_TO_HBAR

    @classmethod
    def from_tinybars(cls, tinybars):
        return cls(tinybars, in_tinybars=True)

    def __str__(self):
        return f"{self.to_hbars():.8f} ℏ"

    def __repr__(self):
        return f"Hbar({self.to_hbars():.8f})"