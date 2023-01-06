import os
from py2neo import Graph
from .query import QueryWrapper


DB_URI = os.getenv('NEO4J_DB_URI')


class GraphDbService:
    def __init__(self, db_uri: str):
        self.db = Graph(db_uri)

    def fetch_peptides(self) -> QueryWrapper:
        query = 'MATCH (n:Peptide) RETURN n.seq'
        return QueryWrapper(self.db.query(query))


db_service = GraphDbService(DB_URI)
