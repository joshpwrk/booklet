import redis

class Instrument:
    def __init__(self, r: redis.Redis, instrument_id: str):
        self.r = r
        self.id = instrument_id

    # TODO: eventually would be nice to sort by entry time
    def get_orders_within_limit_price(is_bid: bool, limit_price: float, max_counteparties: int) -> List(str):
        # use redis z sets to get all orders within range
        order_ids = self.r.zrangebyscore(
            _redis_price_set(self.id, is_bid), 
            min="-inf", max=limit_price, 
            start=0, max_counteparties
        )

        # prune out the ones that expired in one redis operation
        # (note this doesn't clear the orderedsets)
        pipe = self.r.pipeline()
        for id in order_ids:
            pipe.exists(id)
        results = exists_pipeline.execute()
        return [order_ids[i] for i, result in enumerate(results) if result == 1]

    def get_expired_orders(is_bid: bool) -> List(str):
        expiry_zset_key = _redis_expiry_set(self.id, is_bid)

        expired_order_ids = self.r.zrangebyscore(
            expiry_zset_key, 
            min_score=-inf, 
            max_score=int(datetime.datetime.now().timestamp())
        )

        return order_ids 

    def redis_price_set(self, is_bid: bool):
        return self.id + ('-BID' if is_bid else '-ASK') + "-" + "BY_PRICE"
    
    def redis_expiry_set(self, is_bid: bool):
        self.id + ('-BID' if is_bid else '-ASK') + "-" + "BY_EXPIRY"
        

