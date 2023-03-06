import json
import uuid
import redis

class LimitOrder:
    def __init__(self, json_str: str):
        self.json_str = json_str

        self.json = json.loads(json_str)
        self.user = json_dict['user']
        self.is_bid = json_dict['is_bid']
        self.limit_price = json_dict['limit_price']
        self.amount = json_dict['amount']
        self.order_expiry = json_dict['order_expiry']
        self.instrument_id = 'ETH-$1300-CALL-01012024'
        self.order_id = uuid.uuid4()
