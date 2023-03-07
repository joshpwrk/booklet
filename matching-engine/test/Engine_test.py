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

    def test_post_non_crossing_limit_orders(self):
        order1_json = {"user": "testuser1", "order_id": "random1", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}
        order2_json = {"user": "testuser2", "order_id": "random2", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}

        # Add the orders to the Redis set
        print("POSTING 1...")
        self.engine.post_limit_order(json.dumps(order1_json))
        print("POSTING 2...")
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

    
    def test_post_crossing_limit_orders(self):
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

        for key in self.engine.r.scan_iter("*"):
            # value = self.engine.r.get(key)
            print(key.decode())

        order1_redis = self.engine.r.get(existing_order1_json["order_id"])
        order2_redis = self.engine.r.get(existing_order2_json["order_id"])

        print(order2_redis)
        print(json.dumps(existing_order2_json))

        self.assertEqual(existing_order1_json, json.loads(order1_redis))
        self.assertEqual(existing_order2_json, json.loads(order2_redis))

        # post limit order that can cross
        order_json = {
            "user": "testuser1", 
            "order_id": "random1", 
            "is_bid": True, 
            "limit_price": 100, 
            "amount": 10, 
            "order_expiry": 1679155437
        }
        
    
        # filled_orders, partial_fill = Engine.pairoff(order, counter_orders)
        
        # self.assertEqual(len(filled_orders), 1)
        # self.assertEqual(filled_orders[0].order_id, "random3")
        # self.assertEqual(partial_fill, None)
        # self.assertEqual(order.amount, 5)
        # self.assertEqual(counter_orders[0].amount, 0)
        # self.assertEqual(counter_orders[1].amount, 0)


if __name__ == '__main__':
    unittest.main()