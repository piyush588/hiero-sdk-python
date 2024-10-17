from src.tokens.token_id import TokenId
from src.account.account_id import AccountId

class TransactionReceipt:
    def __init__(self, receipt_proto):
        self.status = receipt_proto.status
        self._receipt_proto = receipt_proto

    @property
    def tokenId(self):
        """
        Returns the TokenId associated with the transaction receipt, if available.
        """
        if self._receipt_proto.HasField('tokenID') and self._receipt_proto.tokenID.tokenNum != 0:
            return TokenId.from_proto(self._receipt_proto.tokenID)
        else:
            return None

    @property
    def accountId(self):
        """
        Returns the AccountId associated with the transaction receipt, if available.
        """
        if self._receipt_proto.HasField('accountID') and self._receipt_proto.accountID.accountNum != 0:
            return AccountId.from_proto(self._receipt_proto.accountID)
        else:
            return None

    def to_proto(self):
        """
        Returns the underlying protobuf transaction receipt.
        """
        return self._receipt_proto
