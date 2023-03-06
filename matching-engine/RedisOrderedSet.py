from enum import Enum

class RedisOrderedSet(Enum):
    PRICE = "BY_PRICE"
    EXPIRY = "BY_EXPIRY"
    ENTRY = "BY_ENTRY"
