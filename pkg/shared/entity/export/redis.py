from pkg.shared.services.redis.client import RedisService
from pkg.shared.services.redis.async_task import AsyncTaskRedisClientService


_EXPORT_TTL = 60 * 60 * 24


def async_task_redis_client() -> AsyncTaskRedisClientService:
    redis = RedisService.get_instance()
    return AsyncTaskRedisClientService(redis, 'export', _EXPORT_TTL)
