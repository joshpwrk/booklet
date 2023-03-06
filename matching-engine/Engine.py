import json
import uuid
import redis
import LimitOrder from LimitOrder
from .redis_utils import launch_redis_client
from RedisOrderedSet import RedisOrderedSet

class Engine:
    def __init__(self, max_counterparties: int):
        self.r = redis_client = launch_redis_client()
        self.max_counterparties = max_counterparties

    def get_orders_within_limit_price(instrument_id: str, is_bid: bool, limit_price: float) -> LimitOrder:
        order_ids self.r.zrangebyscore(
            _get_redis_db(instrument_id, is_bid, RedisOrderedSet.PRICE), 
            min="-inf", max=limit_price, 
            start=0, self.max_counterparties
        )

        return list(map(lambda x: LimitOrder(x), self.r.mget(order_ids)))

    def _save_to_redis(self, order: LimitOrder):

        self.r.zadd(
            _get_redis_db(order.instrument_id, order.is_bid, RedisOrderedSet.PRICE), 
            {order.order_id: order.limit_price}, 
            CH=True, 
            NX=True
        )

        self.r.zadd(
            _get_redis_db(order.instrument_id, order.is_bid, RedisOrderedSet.ORDEREXPIRY), 
            {order.order_id: order.order_expiry}, 
            CH=True, 
            NX=True
        )

        self.r.set(str(order.order_id), order.json_string)

    def _execute():

    def _get_redis_db(instrument_id: str, is_bid: bool, redis_set: RedisOrderedSet):
        return instrument_id + ('-BID' if order.is_bid else '-ASK') + "-" + redis_set

    def _remove_expired(current_time: int):
        redis.zremrangebyscore("my_sorted_set", max=current_time)




