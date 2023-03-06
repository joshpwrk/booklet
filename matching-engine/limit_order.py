from .redis_utils import launch_redis_client


def post_limit_order():
    redis_client = launch_redis_client()