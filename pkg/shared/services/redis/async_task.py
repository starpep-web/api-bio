import json
from typing import Any
from pkg.shared.utils.lang import safe_json_parse
from pkg.shared.services.redis.client import RedisService


class AsyncTaskRedisClientService:
    def __init__(self, redis: RedisService, key_prefix: str, ttl: int):
        self.redis = redis
        self.key_prefix = key_prefix
        self.ttl = ttl

    def resolve_key(self, task_id: str) -> str:
        return f'{self.key_prefix}:{task_id}'

    def create_task(self, task_id: str, task_data: Any) -> None:
        self.redis.client.set(self.resolve_key(task_id), json.dumps(task_data), ex=self.ttl)

    def update_task(self, task_id: str, task_data: Any) -> None:
        self.redis.client.set(self.resolve_key(task_id), json.dumps(task_data), keepttl=True, xx=True)

    def get_task(self, task_id: str) -> Any:
        cached = self.redis.client.get(self.resolve_key(task_id))
        return safe_json_parse(cached)
