from py2neo import Graph
from pkg.config import config


class GraphDatabaseService:
    instance: 'GraphDatabaseService' = None
    
    def __init__(self):
        self.client = Graph(config.neo4j_db_uri)
    
    @staticmethod
    def get_instance() -> 'GraphDatabaseService':
        if GraphDatabaseService.instance is None:
            GraphDatabaseService.instance = GraphDatabaseService()
            
        return GraphDatabaseService.instance
