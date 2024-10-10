class Hbar:
    TINYBAR = 1
    MICROBAR = 100
    MILLIBAR = 100_000
    HBAR = 100_000_000

    def __init__(self, amount, unit=HBAR):
        self.amount = amount * unit  

    def to_tinybars(self):
        return self.amount

    def to(self, unit):
        return self.amount / unit
