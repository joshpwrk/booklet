import json
import uuid
import redis
from datetime import datetime

class LimitOrder:
    def __init__(self, json_str: str):
        self.json = json.loads(json_str)

        # assign order_id if new order
        if self.json["order_id"] == None:
            self.order_id = uuid.uuid4()
            self.entry_time = datetime.now()
        else:
            self.order_id = self.json["order_id"]
            self.entry_time = self.json["entry_time"]


        self.user = self.json['user']
        self.entry_time = self.json['user']
        self.is_bid = self.json['is_bid']
        self.limit_price = self.json['limit_price']
        self.amount = self.json['amount']
        self.order_expiry = self.json['order_expiry']

        self.instrument_id = 'ETH-$1300-CALL-01012024'

    def delete_from_redis(self, pipe: Redis.Pipeline):
        (price_zset_key, expiry_zset_key) = _redis_orderedsets(order.instrument_id, order.is_bid)

        pipe.zrem(price_zset_key, order.order_id)
        pipe.zrem(expiry_zset_key, order.order_id)
        pipe.delete(order.order_id)
 
    def post_to_redis(self, pipe: Redis.Pipeline):
        (price_zset_key, expiry_zset_key) = _redis_orderedsets(order.instrument_id, order.is_bid)

        pipe.zadd(price_zset_key, {order.order_id: order.limit_price}, CH=True, NX=True)
        pipe.zadd(expiry_zset_key, {order.order_id: order.order_expiry}, CH=True, NX=True)
        pipe.set(order.order_id, json.dumps(self.json))

        # automatically clears expired orders in main set
        # but need periodic runners to clear the price and expiry zsets
        pipe.expireat(order.order_id, order.order_expiry)
