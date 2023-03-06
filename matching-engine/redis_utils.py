import redis

def launch_redis_client(host='localhost', port=6379):
    """
    Launch a Redis client and return the client object.

    Parameters:
    host (str): The Redis server hostname or IP address (default is 'localhost').
    port (int): The Redis server port number (default is 6379).

    Returns:
    redis.Redis: A Redis client object connected to the specified Redis server.
    """
    client = redis.Redis(host=host, port=port)
    return client