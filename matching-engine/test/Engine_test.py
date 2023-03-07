import unittest
from ..Engine import Engine
import uuid
from ..LimitOrder import LimitOrder
import json 
import subprocess
import os

# run with: `python -m unittest -v matching-engine/test/Engine_test.py`
class EngineTest(unittest.TestCase):
    def setUp(self):
        redis_config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'redis.conf')
        redis_log_file = os.path.join(os.path.dirname(__file__), "enginge_test_redis.log")
        
        print("LAUNCHING REDIS...")
        launch_redis = subprocess.Popen(['redis-server', redis_config_path, '--logfile', redis_log_file])

        print("LAUNCHING ENGINE...")
        self.engine = Engine(max_counterparties=5)

    def test_post_non_crossing_limit_orders(self):
        order1_json = {"user": "testuser1", "order_id": "random1", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}
        order2_json = {"user": "testuser2", "order_id": "random2", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}

        # Add the orders to the Redis set
        print("POSTING 1...")
        print(json.dumps(order1_json))
        self.engine.post_limit_order(json.dumps(order1_json))
        print("POSTING 2...")
        print(json.dumps(order2_json))
        self.engine.post_limit_order(json.dumps(order2_json))

        # Check that the orders were added correctly
        order1_from_redis = self.engine.r.get(order1_json["order_id"])
        order2_from_redis = self.engine.r.get(order2_json["order_id"])

        print("PRINT ALL KEYS...")
        for key in self.engine.r.scan_iter("*"):
            # value = self.engine.r.get(key)
            print(key.decode())

        self.assertEqual(order1_json, json.loads(order1_from_redis))
        self.assertEqual(order2_json, json.loads(order2_from_redis))

if __name__ == '__main__':
    unittest.main()