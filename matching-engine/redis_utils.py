import redis

def launch_redis_client(host='localhost', port=6379):
    client = redis.Redis(host=host, port=port)
    return client