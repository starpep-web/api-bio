import os
from dataclasses import dataclass


@dataclass
class Config:
    redis_uri: str
    neo4j_db_uri: str

    assets_location: str
    temp_artifacts_location: str

    @staticmethod
    def from_env() -> 'Config':
        return Config(
            redis_uri=os.getenv('REDIS_URI'),
            neo4j_db_uri=os.getenv('NEO4J_DB_URI'),
            assets_location=os.getenv('ASSETS_LOCATION'),
            temp_artifacts_location=os.getenv('TEMP_ARTIFACTS_LOCATION'),
        )


config = Config.from_env()
