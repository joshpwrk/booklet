import json
import uuid
import redis
import LimitOrder from LimitOrder
from .redis_utils import launch_redis_client
from RedisOrderedSet import RedisOrderedSet
from datetime import datetime

# The engine uses a dual DB model in redis:
# 1) OrderQueue which is added to by any websocket implementation
# 2) OrderBook which holds all the outstanding limit orders

# Having an orderqueue reduces alot of headaches with preventing race conditions.
# Another benefit is that the websocket and matching-engine can be swapped out.
class Engine:
    def __init__(self, max_counterparties: int):
        self.r = redis_client = launch_redis_client()
        self.max_counterparties = max_counterparties

    ########
    # POST #
    ########

    def post_limit_order(limit_order: str):
        order = LimitOrder(limit_order)


        # Get the best counterparties for the order
        counter_orders = self.get_orders_within_limit_price(
            order.instrument_id, not order.is_bid, order.limit_price)[:self.max_counterparties]

        # Begin pipe to batch all redis writes into atomic transaction
        pipe = self.r.pipeline()

        # Execute the order against the best counterparties
        if counter_orders:
            counter_orders = list(map(lambda x: LimitOrder(x), self.r.mget(counter_orders))) 
            (filled_orders, partial_fill) = self._pairoff(order, counter_orders)

            # delete filled orders from redis
            [order.delete_from_redis(pipe) for order in filled_orders]
            # update partial filled order
            partial_fill.post_to_redis(pipe)

        # Save whatever is left to redis
        if order.amount > 0:
            order.post_to_redis(pipe)
        
        # Execute atomically in one transaction
        pipe.execute()
        
    #######
    # GET #
    #######

    # TODO: eventually would be nice to sort by entry time
    def get_orders_within_limit_price(instrument_id: str, is_bid: bool, limit_price: float) -> LimitOrder:
        # use redis z sets to get all orders within range
        order_ids = self.r.zrangebyscore(
            _redis_subset_name(instrument_id, is_bid, RedisOrderedSet.PRICE), 
            min="-inf", max=limit_price, 
            start=0, self.max_counterparties
        )

        # prune out the ones that expired in one redis operation
        # (note this doesn't clear the orderedsets)
        pipe = self.r.pipeline()
        for id in order_ids:
            pipe.exists(id)
        results = exists_pipeline.execute()
        return [order_ids[i] for i, result in enumerate(results) if result == 1]

    def get_expired_orders(instrument_id: str, is_bid: bool):
        (, expiry_zset_key) = _redis_orderedsets(order.instrument_id, order.is_bid)

        expired_order_ids = self.r.zrangebyscore(
            expiry_zset_key, 
            min_score=-inf, 
            max_score=int(datetime.datetime.now().timestamp())
        )

        return order_ids 
          
    ##################
    # BUSINESS LOGIC #
    ##################
        
    # Change to BaseOrder so that can be reused in pairing off market orders
    def _pairoff(order: LimitOrder, counter_orders: List[LimitOrder]) -> (List[str], LimitOrder):
        filled_orders = []
    
        # Loop through counter orders and execute against input order
        for counter_order in counter_orders:
            # Execute as much of the order as possible
            amount = min(order.amount, counter_order.amount)
            order.amount -= amount
            counter_order.amount -= amount
            
            # If counter order has been fully executed, mark it for deletion
            if counter_order.amount == 0:
                filled_orders.append(counter_order)
            
            # If input order has been fully executed, exit loop and mark it for modification
            if order.amount == 0:
                break
        
        partial_fill = counter_order if counter_order.amount != 0 else None

        # Return orders to delete and order to modify
        return filled_orders, partial_fill

    def _redis_orderedsets(instrument_id: str, is_bid: bool):
        return (
            instrument_id + ('-BID' if order.is_bid else '-ASK') + "-" + RedisOrderedSet.PRICE,
            instrument_id + ('-BID' if order.is_bid else '-ASK') + "-" + RedisOrderedSet.EXPIRY
        )




