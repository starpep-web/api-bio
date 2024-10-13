from typing import Optional, Iterable
from py2neo import Graph
from .query import QueryWrapper
from .models import SearchResultPeptide, FullPeptide

class PeptideDatabaseService:
    def __init__(self, service: GraphDatabaseService):
        self.service = service

    def get_all_peptides(self) -> QueryWrapper[Iterable[SearchResultPeptide]]:
        query = 'MATCH (n:Peptide)-[]->(v:Attributes) RETURN ID(n) as id, n.seq as seq, SIZE(n.seq) as length, v as attributes ORDER BY id ASC'

        def mapper(wrapper: QueryWrapper[Iterable[SearchResultPeptide]]) -> Iterable[SearchResultPeptide]:
            try:
                cur = wrapper.cursor.next()

                while cur is not None:
                    yield SearchResultPeptide.from_neo4j_properties(cur)
                    cur = wrapper.cursor.next()
            except StopIteration:
                return

        return QueryWrapper(self.service.db.query(query), mapper)

