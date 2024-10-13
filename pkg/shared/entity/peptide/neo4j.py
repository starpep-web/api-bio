from typing import Iterable
from pkg.shared.entity.peptide.models import SearchPeptide
from pkg.shared.services.neo4j.client import GraphDatabaseService
from pkg.shared.services.neo4j.query import QueryWrapper


def get_all_peptides() -> QueryWrapper[Iterable[SearchPeptide]]:
    db = GraphDatabaseService.get_instance()
    query = 'MATCH (n:Peptide)-[]->(v:Attributes) RETURN ID(n) as id, n.seq as seq, SIZE(n.seq) as length, v as attributes ORDER BY id ASC'

    def mapper(wrapper: QueryWrapper[Iterable[SearchPeptide]]) -> Iterable[SearchPeptide]:
        try:
            cur = wrapper.cursor.next()

            while cur is not None:
                yield SearchPeptide.from_neo4j_properties(cur)
                cur = wrapper.cursor.next()
        except StopIteration:
            return

    return QueryWrapper(db.client.query(query), mapper)
