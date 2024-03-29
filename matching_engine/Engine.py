import json
import uuid
import redis
from .LimitOrder import LimitOrder
from .Instrument import Instrument
from .util import launch_redis_client
from datetime import datetime
import time

# The engine uses a dual DB model in redis:
# 1) OrderBook: self.orderbook which holds all the outstanding limit orders
# 2) Queue: self.queue which is added to by any websocket implementation
# 3) Settlement: queue of orders waiting to be settled on chain

class Engine:
    def __init__(self, max_counterparties: int):
        self.orderbook = redis_client = launch_redis_client(db=0)
        self.queue = redis_client = launch_redis_client(db=1)
        self.settlement = redis_client = launch_redis_client(db=2)
        self.run_flag = False

        self.max_counterparties = max_counterparties
        self.orders_processed = 0
        self.orders_matched = 0

    #########
    # QUEUE #
    #########

    def consume_queue(self):
        print("Consuming Queue...")
        self.run_flag = True
        while self.run_flag:
            # Read all items in the zset
            items = self.queue.zrange("queue", 0, -1, withscores=False)
            
            if items:
                # Process each item
                for item in items:
                    # Convert the item from bytes to string
                    item = item.decode('utf-8')

                    # Process the item
                    self.post_limit_order(item)

                    self.orders_processed += 1
        
                # Remove all processed items from the zset
                self.queue.zrem("queue", *items)

                print("orders processed:", self.orders_processed, datetime.now())
                print("orders matched:", self.orders_matched, datetime.now())

    ########
    # POST #
    ########

    def post_limit_order(self, limit_order: str):
        order = LimitOrder(limit_order)
        original_amount = order.amount

        # Clear out all expired orders
        instrument = Instrument(self.orderbook, order.instrument_id)
        self.clear_expired(instrument, order.is_bid)

        # Get the best counterparties for the order
        counter_orders = instrument.get_crossable_orders(
            not order.is_bid, 
            order.limit_price, 
            self.max_counterparties
        )

        # Begin pipe to batch all redis writes into atomic transaction
        ob_pipe = self.orderbook.pipeline()
        s_pipe = self.settlement.pipeline()

        # Execute the order against the best counterparties
        if counter_orders:
            counter_orders = list(map(lambda x: LimitOrder(x), self.orderbook.mget(counter_orders))) 
            (filled_orders, partial_fill) = self.pairoff(order, counter_orders)
            self.orders_matched += len(filled_orders) + 1

            # delete filled orders from redis
            [f_order.delete_from_redis(ob_pipe) for f_order in filled_orders]

            # add to settlement queue
            [f_order.post_to_settlement(s_pipe, f_order.amount, [order.order_id]) for f_order in filled_orders]

            # update partial filled order
            if partial_fill:
                partial_fill.post_to_redis(ob_pipe)
                all_counter_parties = [partial_fill.order_id]
                # TODO: post partial fill with proper amount to settlement
            else:
                all_counter_parties = []
            
            # post main order to settlement queue
            all_counter_parties += [order.order_id for order in filled_orders]

            order.post_to_settlement(s_pipe, original_amount - order.amount, all_counter_parties)

        # Save whatever is left to redis
        # TODO: just leaves a "cross-able" order
        #       thus violating the "always" cross rule
        if order.amount > 0:
            order.post_to_redis(ob_pipe)
        
        # Execute atomically in one transaction
        ob_pipe.execute()
        s_pipe.execute()

    ##################
    # BUSINESS LOGIC #
    ##################

    def clear_expired(self, instrument, is_bid):
        expired_ids = self.orderbook.zrangebyscore(
            instrument.redis_expiry_set(instrument.id, is_bid),
            min="-inf",
            max=int(time.time())
        )
        expired_orders = list(map(lambda x: LimitOrder(x), self.orderbook.mget(expired_ids))) 

        pipe = self.orderbook.pipeline()
        for order in expired_orders:
            order.delete_from_redis(pipe)
        results = pipe.execute()
        
    # Change to BaseOrder so that can be reused in pairing off market orders
    @staticmethod
    def pairoff(order: LimitOrder, counter_orders: list[LimitOrder]):
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




