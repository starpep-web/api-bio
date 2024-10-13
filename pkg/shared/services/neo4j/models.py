from abc import ABC, abstractmethod
from typing import Dict, Any


class Neo4jModel(ABC):
    @staticmethod
    @abstractmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'Neo4jModel':
        pass
