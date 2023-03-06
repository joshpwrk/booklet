import json
import uuid
import redis

class LimitOrder:
    def __init__(self, user: int, is_bid: bool, limit_price: float, amount: float, order_expiry: int):
        self.user = user
        self.is_bid = is_bid
        self.limit_price = limit_price
        self.amount = amount
        self.order_expiry = order_expiry
        self.instrument_id = 'ETH-$1300-CALL-01012024' # add some protected way of adding instruments.  
        self.order_id = uuid.uuid4()

    def __init__(self, json_str: str):
        self.json = json.loads(json_str)
        self.user = json_dict['user']
        self.is_bid = json_dict['is_bid']
        self.limit_price = json_dict['limit_price']
        self.amount = json_dict['amount']
        self.order_expiry = json_dict['order_expiry']
        self.instrument_id = 'ETH-$1300-CALL-01012024'
        self.order_id = uuid.uuid4()

    def save_to_redis(self, redis_client: redis.Redis):
        json_string = json.dumps(self.json)

        redis_client.zadd(
            self.instrument_id + ('-BID' if self.isBid else '-ASK') + "-BYPRICE", 
            {self.order_id: self.limit_price}, 
            CH=True, 
            NX=True
        )

        redis_client.zadd(
            self.instrument_id + ('-BID' if self.isBid else '-ASK') + "-BYORDEREXPIRY", 
            {self.order_id: self.order_expiry}, 
            CH=True, 
            NX=True
        )

        redis_client.set(str(self.order_id), json_string)
