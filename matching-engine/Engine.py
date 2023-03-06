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
        instrument = Instrument(self.r, order.instrument_id)
        counter_orders = instrument.get_orders_within_limit_price(
            order.is_bid, 
            order.limit_price, 
            self.max_counterparties
        )

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




