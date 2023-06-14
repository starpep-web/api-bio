from typing import List, Optional
from dataclasses import dataclass
from Bio.Align import substitution_matrices, PairwiseAligner
from database.models import Peptide


_BLOSUM_MATRIX_NAMES = ('BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90')


@dataclass
class AlignedPeptide(Peptide):
    score: float


def replace_atypical_aas(seq: str) -> str:
    return seq.replace('O', 'K').replace('J', 'L').replace('U', 'C')


# TODO: Accept options
def _align_query_with_matrix(substitution_matrix: Optional[List[str]], database: List[Peptide], query: str) -> List[AlignedPeptide]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrix
    aligner.mode = 'global'

    max_score = sum([aligner.substitution_matrix[a, a] for a in query])

    result = []
    for target in database:
        score = aligner.score(replace_atypical_aas(target.sequence), query)
        score_ratio = score / float(max_score)

        result.append(AlignedPeptide(target.id, target.sequence, target.length, score_ratio))

    result.sort(key=lambda n: -n.score)

    return result


def blosum_align_query(blosum_type: str, database: List[Peptide], query: str) -> List[AlignedPeptide]:
    if blosum_type not in _BLOSUM_MATRIX_NAMES:
        raise Exception(f'{blosum_type} is not a valid BLOSUM matrix type.')

    substitution_matrix = substitution_matrices.load(blosum_type)
    return _align_query_with_matrix(substitution_matrix, database, query)
