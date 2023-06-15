import os
from .redis import RedisClientService


cache = RedisClientService(os.getenv('REDIS_URI'))
