from typing import Any
import redis
import json


REDIS_TTL = 60 * 60  # 1 Hour


class RedisClientService:
    def __init__(self, uri: str):
        self.redis = redis.from_url(uri)
        self.search = SearchRedisClientService(self)


class SearchRedisClientService:
    KEY_PREFIX = 'search'

    def __init__(self, service: RedisClientService):
        self.service = service

    def create_task(self, task_id: str, task_data: Any) -> None:
        self.service.redis.set(SearchRedisClientService.resolve_key(task_id), json.dumps(task_data), ex=REDIS_TTL)

    def update_task(self, task_id: str, task_data: Any) -> None:
        self.service.redis.set(SearchRedisClientService.resolve_key(task_id), json.dumps(task_data), keepttl=True, xx=True)

    def get_task(self, task_id: str) -> Any:
        cached = self.service.redis.get(SearchRedisClientService.resolve_key(task_id))
        return json.loads(cached) if cached is not None else None

    @staticmethod
    def resolve_key(task_id: str) -> str:
        return f'{SearchRedisClientService.KEY_PREFIX}:{task_id}'
