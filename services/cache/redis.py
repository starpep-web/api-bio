from typing import Any
import redis
import json


_TTL_ONE_HOUR = 60 * 60
_TTL_ONE_DAY = _TTL_ONE_HOUR * 24


class RedisClientService:
    def __init__(self, uri: str):
        self.redis = redis.from_url(uri)
        self.search = AsyncTaskRedisClientService(self, 'search', _TTL_ONE_HOUR)
        self.export = AsyncTaskRedisClientService(self, 'export', _TTL_ONE_DAY)


class AsyncTaskRedisClientService:
    def __init__(self, service: RedisClientService, key_prefix: str, ttl: int):
        self.service = service
        self.key_prefix = key_prefix
        self.ttl = ttl

    def resolve_key(self, task_id: str) -> str:
        return f'{self.key_prefix}:{task_id}'

    def create_task(self, task_id: str, task_data: Any) -> None:
        self.service.redis.set(self.resolve_key(task_id), json.dumps(task_data), ex=self.ttl)

    def update_task(self, task_id: str, task_data: Any) -> None:
        self.service.redis.set(self.resolve_key(task_id), json.dumps(task_data), keepttl=True, xx=True)

    def get_task(self, task_id: str) -> Any:
        cached = self.service.redis.get(self.resolve_key(task_id))
        return json.loads(cached) if cached is not None else None
