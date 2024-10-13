import redis
from pkg.config import config


class RedisService:
    instance: 'RedisService' = None

    def __init__(self):
        self.client = redis.from_url(config.redis_uri)

    @staticmethod
    def get_instance() -> 'RedisService':
        if RedisService.instance is None:
            RedisService.instance = RedisService()

        return RedisService.instance
