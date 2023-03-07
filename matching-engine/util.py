import redis
import time

def launch_redis_client(host='localhost', port=6379, db=0):
    r = redis.Redis(host=host, port=port, db=db)
    while True:
        try:
            r.ping()
            break
        except redis.exceptions.ConnectionError:
            time.sleep(0.1)

    return r

