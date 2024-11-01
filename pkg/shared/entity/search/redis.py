from pkg.shared.services.redis.client import RedisService
from pkg.shared.services.redis.async_task import AsyncTaskRedisClientService


_SEARCH_TTL = 60 * 60


def get_async_task_redis_client() -> AsyncTaskRedisClientService:
    redis = RedisService.get_instance()
    return AsyncTaskRedisClientService(redis, 'search', _SEARCH_TTL)
