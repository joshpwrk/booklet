import redis
import time 

class Instrument:
    def __init__(self, r: redis.client.Redis, instrument_id: str):
        self.orderbook = r
        self.id = instrument_id

    # TODO: sort by entry time within same price
    def get_crossable_orders(self, is_bid: bool, limit_price: float, max_counteparties: int):
        # use redis z sets to get all orders within range
        # TODO: should loop back in and find more counter_parties if all expired
        order_ids = self.orderbook.zrangebyscore(
            self.redis_price_set(self.id, is_bid),
            min= limit_price if is_bid else "-inf", 
            max= "inf" if is_bid else limit_price, 
            start=0, num=max_counteparties
        )

        # automatically return asc vs desc order depending on type
        # if (is_bid): order_ids = order_ids[::-1]

        return order_ids if is_bid else order_ids[::-1]

    def get_orders_in_tick(self, is_bid: bool, tickMin, tickMax):
        # use redis z sets to get all orders within range
        # TODO: assumes all orders are expired - but engine only clears whenever there is a new request
        return self.orderbook.zrangebyscore(
            self.redis_price_set(self.id, is_bid),
            min= tickMin,
            max= tickMax
        )


    @staticmethod
    def redis_price_set(instrument_id: str, is_bid: bool):
        return instrument_id + ('-BID' if is_bid else '-ASK') + "-" + "BY_PRICE"

    @staticmethod
    def redis_expiry_set(instrument_id: str, is_bid: bool):
        return instrument_id + ('-BID' if is_bid else '-ASK') + "-" + "BY_EXPIRY"
        

