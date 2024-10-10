from src.outputs import basic_types_pb2

class TokenId:
    def __init__(self, shard=0, realm=0, num=0):
        self.shard = shard
        self.realm = realm
        self.num = num

    @classmethod
    def from_string(cls, token_id_str):
        parts = token_id_str.strip().split('.')
        if len(parts) == 3:
            shard, realm, num = map(int, parts)
            return cls(shard, realm, num)
        else:
            raise ValueError("Invalid token ID format, expected 'shard.realm.tokenNum'")

    def to_proto(self):
        token_id = basic_types_pb2.TokenID()
        token_id.shardNum = self.shard
        token_id.realmNum = self.realm
        token_id.tokenNum = self.num
        return token_id

    def __str__(self):
        return f"{self.shard}.{self.realm}.{self.num}"