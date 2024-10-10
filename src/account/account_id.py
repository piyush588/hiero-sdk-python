from src.outputs import basic_types_pb2

class AccountId:
    def __init__(self, shard=0, realm=0, num=0):
        self.shard = shard
        self.realm = realm
        self.num = num

    @classmethod
    def from_string(cls, account_id_str):
        parts = account_id_str.strip().split('.')
        if len(parts) != 3:
            raise ValueError("Invalid account ID format, expected 'shard.realm.account'")
        shard, realm, num = map(int, parts)
        return cls(shard, realm, num)

    def to_proto(self):
        account_id = basic_types_pb2.AccountID()
        account_id.shardNum = self.shard
        account_id.realmNum = self.realm
        account_id.accountNum = self.num
        return account_id

    def __str__(self):
        return f"{self.shard}.{self.realm}.{self.num}"
