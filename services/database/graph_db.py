from typing import Optional, Iterable
from py2neo import Graph
from .query import QueryWrapper
from .models import Peptide, FullPeptide


class GraphDatabaseService:
    def __init__(self, uri: str):
        self.db = Graph(uri)
        self.peptides = PeptideDatabaseService(self)


class PeptideDatabaseService:
    def __init__(self, service: GraphDatabaseService):
        self.service = service

    def get_all_peptides(self) -> QueryWrapper[Iterable[Peptide]]:
        query = 'MATCH (n:Peptide) RETURN ID(n) as id, n.seq as seq, SIZE(n.seq) as length ORDER BY id ASC'

        def mapper(wrapper: QueryWrapper[Iterable[Peptide]]) -> Iterable[Peptide]:
            try:
                cur = wrapper.cursor.next()

                while cur is not None:
                    yield Peptide.from_dict(cur)
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

            for row in data:
                relationship = type(row[3]).__name__
                value = row[4].get('name')

                if relationship in metadata_dict:
                    metadata_dict[relationship].append(value)
                else:
                    metadata_dict[relationship] = [value]

            return FullPeptide.from_dict({**peptide_dict, **metadata_dict})

        params = {
            'sequence': sequence.upper()
        }
        return QueryWrapper(self.service.db.query(query, params), mapper)
