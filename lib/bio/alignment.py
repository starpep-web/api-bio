from typing import List, Optional
from Bio.Align import substitution_matrices, PairwiseAligner
from database.models import Peptide


_BLOSUM_MATRIX_NAMES = ('BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90')


def replace_atypical_aas(seq: str) -> str:
    # TODO: Refactor this to replace in 1 iteration instead of 3.
    return seq.replace('O', 'K').replace('J', 'L').replace('U', 'C')


# TODO: Type the return value of this function.
def _align_query_with_matrix(substitution_matrix: Optional[List[str]], database: List[Peptide], query: str) -> List[str]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrix
    aligner.mode = 'local'

    result = []
    for target in database:
        score = aligner.score(replace_atypical_aas(target.sequence), query)

        result.append((target, score))

    result.sort(key=lambda n: -n[1])

    return result


def blosum_align_query(blosum_type: str, database: List[Peptide], query: str) -> List[str]:
    if blosum_type not in _BLOSUM_MATRIX_NAMES:
        raise Exception(f'{blosum_type} is not a valid BLOSUM matrix type.')

    substitution_matrix = substitution_matrices.load(blosum_type)
    return _align_query_with_matrix(substitution_matrix, database, query)
