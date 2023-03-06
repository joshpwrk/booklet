import redis

def launch_redis_client(host='localhost', port=6379, db=0):
    client = redis.Redis(host=host, port=port, db=db)
    return client