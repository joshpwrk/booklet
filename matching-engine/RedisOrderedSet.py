from enum import Enum

class RedisOrderedSet(Enum):
    PRICE = "BY_PRICE"
    ORDEREXPIRY = "BY_ORDER_EXPIRY"
