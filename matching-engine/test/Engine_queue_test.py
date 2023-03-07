import unittest
from ..Engine import Engine
import uuid
from ..LimitOrder import LimitOrder
from ..redis_utils import launch_redis_client
import json 
import subprocess
import os
import time
import threading

# run with: `python -m unittest -v matching-engine/test/Engine__queue_test.py`
class EngineQueueTest(unittest.TestCase):
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

    def test_read_queue(self):
        # Start parallel thread simulating web-socket pushing to queue
        queue_push_thread = threading.Thread(target=EngineQueueTest.push_to_queue)
        queue_push_thread.start()

        # Check that the orders were added correctly
        self.engine.consume_queue()

    @classmethod
    def push_to_queue(cls):
        queue_push_client = launch_redis_client(db=1)

        # Add the orders to the Redis set
        order1_json = {"user": "testuser1", "order_id": "random1", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}
        order2_json = {"user": "testuser2", "order_id": "random2", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}
        order3_json = {"user": "testuser3", "order_id": "random3", "is_bid": True, "limit_price": 100, "amount": 10, "order_expiry": 1679155437}

        queue_push_client.zadd("queue", {json.dumps(order1_json): round(time.time() * 1000)})
        time.sleep(0.00001) # 10ms
        queue_push_client.zadd("queue", {json.dumps(order2_json): round(time.time() * 1000)})
        time.sleep(0.00001) # 10ms
        queue_push_client.zadd("queue", {json.dumps(order3_json): round(time.time() * 1000)})
        time.sleep(0.00001) # 10ms


if __name__ == '__main__':
    unittest.main()