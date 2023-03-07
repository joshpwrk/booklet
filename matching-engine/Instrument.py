import redis

class Instrument:
    def __init__(self, r: redis.client.Redis, instrument_id: str):
        self.r = r
        self.id = instrument_id

    # TODO: eventually would be nice to sort by entry time
    def get_crossable_orders(self, is_bid: bool, limit_price: float, max_counteparties: int):
        # use redis z sets to get all orders within range
        order_ids = self.r.zrangebyscore(
            self.redis_price_set(self.id, is_bid),
            min= limit_price if is_bid else "-inf", 
            max= "inf" if is_bid else limit_price, 
            start=0, num=max_counteparties
        )
        print("ORDER_IDS")
        print(order_ids)

        # automatically return asc vs desc order depending on type
        if (is_bid):
            order_ids = order_ids[::-1]

        # prune out the ones that expired in one redis operation
        # (note this doesn't clear the orderedsets)
        pipe = self.r.pipeline()
        for id in order_ids:
            pipe.exists(id)
        results = pipe.execute()
        return [order_ids[i] for i, result in enumerate(results) if result == 1]

    def get_expired_orders(is_bid: bool):
        expiry_zset_key = self.redis_expiry_set(self.id, is_bid)

        expired_order_ids = self.r.zrangebyscore(
            expiry_zset_key, 
            min_score=-inf, 
            max_score=int(datetime.datetime.now().timestamp())
        )

        return order_ids 

    @staticmethod
    def redis_price_set(instrument_id: str, is_bid: bool):
        return instrument_id + ('-BID' if is_bid else '-ASK') + "-" + "BY_PRICE"

    @staticmethod
    def redis_expiry_set(instrument_id: str, is_bid: bool):
        return instrument_id + ('-BID' if is_bid else '-ASK') + "-" + "BY_EXPIRY"
        

