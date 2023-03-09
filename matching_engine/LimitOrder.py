import json
import redis
from datetime import datetime
from .Instrument import Instrument

class LimitOrder:
    def __init__(self, json_str: str):
        json_form = json.loads(json_str)        

        self.order_id = json_form["order_id"]
        self.user = json_form['user']
        self.is_bid = json_form['is_bid']
        self.limit_price = json_form['limit_price']
        self.amount = json_form['amount']
        self.order_expiry = json_form['order_expiry']

        self.instrument_id = 'ETH-$1300-CALL-01012024'

        # setup the zset keys
        self.price_zset_key = Instrument.redis_price_set(self.instrument_id, self.is_bid)
        self.expiry_zset_key = Instrument.redis_expiry_set(self.instrument_id, self.is_bid)

    def toJSON(self):
        return {
            "user": self.user,
            "order_id": self.order_id,
            "is_bid": self.is_bid,
            "limit_price": self.limit_price,
            "amount": self.amount,
            "order_expiry": self.order_expiry
        }


    def delete_from_redis(self, pipe: redis.client.Pipeline):
        pipe.zrem(self.price_zset_key, self.order_id)
        pipe.zrem(self.expiry_zset_key, self.order_id)
        pipe.delete(self.order_id)
 
    def post_to_redis(self, pipe: redis.client.Pipeline):
        pipe.zadd(self.price_zset_key, {self.order_id: self.limit_price})
        pipe.zadd(self.expiry_zset_key, {self.order_id: self.order_expiry})
        pipe.set(self.order_id, json.dumps(self.toJSON()))

        # automatically clears expired orders in main set
        # but need periodic runners to clear the price and expiry zsets
        pipe.expireat(self.order_id, self.order_expiry)