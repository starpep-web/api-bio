import os
from dataclasses import dataclass


@dataclass
class Config:
    redis_uri: str
    neo4j_db_uri: str

    @staticmethod
    def from_env() -> 'Config':
        return Config(
            redis_uri=os.getenv('REDIS_URI'),
            neo4j_db_uri=os.getenv('NEO4J_DB_URI'),
        )


config = Config.from_env()
