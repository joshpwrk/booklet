import json
import redis
from datetime import datetime
from .Instrument import Instrument

class LimitOrder:
    def __init__(self, json_str: str):
        self.json = json.loads(json_str)

        # assign order_id if new order
        if self.json.get("entry_time") == None:
            self.entry_time = datetime.now()
        else:
            self.entry_time = self.json["entry_time"]

        self.order_id = self.json["order_id"]
        self.user = self.json['user']
        self.entry_time = self.json['user']
        self.is_bid = self.json['is_bid']
        self.limit_price = self.json['limit_price']
        self.amount = self.json['amount']
        self.order_expiry = self.json['order_expiry']

        self.instrument_id = 'ETH-$1300-CALL-01012024'

        # setup the zset keys
        self.price_zset_key = Instrument.redis_price_set(self.instrument_id, self.is_bid)
        self.expiry_zset_key = Instrument.redis_expiry_set(self.instrument_id, self.is_bid)

    def delete_from_redis(self, pipe: redis.client.Pipeline):
        pipe.zrem(self.price_zset_key, self.order_id)
        pipe.zrem(self.expiry_zset_key, self.order_id)
        pipe.delete(self.order_id)
 
    def post_to_redis(self, pipe: redis.client.Pipeline):
        pipe.zadd(self.price_zset_key, {self.order_id: self.limit_price})
        pipe.zadd(self.expiry_zset_key, {self.order_id: self.order_expiry})
        pipe.set(self.order_id, json.dumps(self.json))

        # automatically clears expired orders in main set
        # but need periodic runners to clear the price and expiry zsets
        pipe.expireat(self.order_id, self.order_expiry)