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
        redis_config_path = os.path.join(os.path.dirname(__file__), 'redis_test.conf')
        redis_log_file = os.path.join(os.path.dirname(__file__), "engine_test_redis.log")
        
        print("LAUNCHING REDIS...")
        self.redis_server = subprocess.Popen(['redis-server', redis_config_path, '--logfile', redis_log_file])

        print("LAUNCHING ENGINE...")
        self.engine = Engine(max_counterparties=5)

    def tearDown(self):
        print("SHUT DOWN REDIS...")
        self.redis_server.terminate()
        self.redis_server.wait()

    def test_post_non_crossing(self):
        order1_json = {"user": "testuser1", "order_id": "random1", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}
        order2_json = {"user": "testuser2", "order_id": "random2", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}

        # Add the orders to the Redis set
        self.engine.post_limit_order(json.dumps(order1_json))
        self.engine.post_limit_order(json.dumps(order2_json))

        # Check that the orders were added correctly
        order1_from_redis = self.engine.r.get(order1_json["order_id"])
        order2_from_redis = self.engine.r.get(order2_json["order_id"])

        # print("PRINT ALL KEYS...")
        # for key in self.engine.r.scan_iter("*"):
        #     # value = self.engine.r.get(key)
        #     print(key.decode())

        self.assertEqual(order1_json, json.loads(order1_from_redis))
        self.assertEqual(order2_json, json.loads(order2_from_redis))

    
    def test_post_crossing(self):
        # post initial orders
        existing_order1_json = {
            "user": "testuser1", 
            "order_id": "random1", 
            "is_bid": False, 
            "limit_price": 90, 
            "amount": 5, 
            "order_expiry": 1679155437
        }

        existing_order2_json = {
            "user": "testuser2", 
            "order_id": "random2", 
            "is_bid": False, 
            "limit_price": 110, 
            "amount": 5, 
            "order_expiry": 1679155437
        }
        self.engine.post_limit_order(json.dumps(existing_order1_json))
        self.engine.post_limit_order(json.dumps(existing_order2_json))

        order1_redis = self.engine.r.get(existing_order1_json["order_id"])
        order2_redis = self.engine.r.get(existing_order2_json["order_id"])

        self.assertEqual(existing_order1_json, json.loads(order1_redis))
        self.assertEqual(existing_order2_json, json.loads(order2_redis))

        # post limit order that can cross
        order_json = {
            "user": "testuser3", 
            "order_id": "random3", 
            "is_bid": True, 
            "limit_price": 100, 
            "amount": 10, 
            "order_expiry": 1679155437
        }
        self.engine.post_limit_order(json.dumps(order_json))
        order_redis = json.loads(self.engine.r.get(order_json["order_id"]))

        self.assertEqual(order_redis["amount"], 5)
        self.assertEqual(self.engine.r.exists("random1"), False)
        self.assertEqual(self.engine.r.exists("random2"), True)

    def test_post_partial_crossing(self):
        # post initial orders
        existing_order1_json = {
            "user": "testuser1", 
            "order_id": "random1", 
            "is_bid": False, 
            "limit_price": 90, 
            "amount": 5, 
            "order_expiry": 1679155437
        }

        existing_order2_json = {
            "user": "testuser2", 
            "order_id": "random2", 
            "is_bid": False, 
            "limit_price": 110, 
            "amount": 5, 
            "order_expiry": 1679155437
        }
        self.engine.post_limit_order(json.dumps(existing_order1_json))
        self.engine.post_limit_order(json.dumps(existing_order2_json))

        order1_redis = self.engine.r.get(existing_order1_json["order_id"])
        order2_redis = self.engine.r.get(existing_order2_json["order_id"])

        self.assertEqual(existing_order1_json, json.loads(order1_redis))
        self.assertEqual(existing_order2_json, json.loads(order2_redis))

        # post limit order that can cross
        order_json = {
            "user": "testuser3", 
            "order_id": "random3", 
            "is_bid": True, 
            "limit_price": 120, 
            "amount": 7, 
            "order_expiry": 1679155437
        }
        self.engine.post_limit_order(json.dumps(order_json))

        # confirm not all orders are crossed
        self.assertEqual(self.engine.r.exists("random3"), False)
        self.assertEqual(self.engine.r.exists("random1"), False)
        self.assertEqual(self.engine.r.exists("random2"), True)
        self.assertEqual(3, json.loads(self.engine.r.get("random2"))["amount"])


if __name__ == '__main__':
    unittest.main()