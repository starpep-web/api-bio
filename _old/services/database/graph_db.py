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

    def get_full_peptide(self, sequence: str) -> QueryWrapper[Optional[FullPeptide]]:
        query = 'MATCH (n:Peptide { seq: $sequence })-[r]->(v) RETURN ID(n) as id, n.seq as seq, SIZE(n.seq) as length, r, v'

        def mapper(wrapper: QueryWrapper[Optional[FullPeptide]]) -> Optional[FullPeptide]:
            data = wrapper.as_np()

            if data.shape[0] < 1:
                return None

            peptide_dict = {
                'id': data[0, 0],
                'seq': data[0, 1],
                'length': data[0, 2]
            }

            metadata_dict = dict()
            attributes_dict = dict()

            for row in data:
                relationship = type(row[3]).__name__

                if relationship == 'characterized_by':
                    attributes_dict = dict(row[4])
                else:
                    value = row[4].get('name')

                    if relationship in metadata_dict:
                        metadata_dict[relationship].append(value)
                    else:
                        metadata_dict[relationship] = [value]

            return FullPeptide.from_neo4j_properties({**peptide_dict, **metadata_dict, 'attributes': attributes_dict})

        params = {
            'sequence': sequence.upper()
        }
        return QueryWrapper(self.service.db.query(query, params), mapper)
