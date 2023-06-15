from __future__ import annotations
from typing import Iterable, Optional, Dict, Any, List
from dataclasses import dataclass
from Bio.Align import substitution_matrices, PairwiseAligner
from services.database.models import Peptide


# TODO: Revise all matrices that work.
# TODO: Improve options validation.
# TODO: Implement multi alignment
_BLOSUM_MATRIX_NAMES = ('BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90')


@dataclass
class SingleAlignedPeptide(Peptide):
    score: float


@dataclass
class SingleAlignmentOptions:
    alg: str
    matrix: str
    threshold: float
    max_quantity: Optional[int]

    @staticmethod
    def create_from_params(params: Dict[str, Any]) -> SingleAlignmentOptions:
        alg = params.get('alg', 'local')
        matrix = params.get('matrix', 'BLOSUM62')
        threshold = params.get('threshold', None)
        threshold = float(threshold) if threshold else 1.0
        max_quantity = params.get('max_quantity', None)
        max_quantity = int(max_quantity) if max_quantity else None

        if alg and alg != 'local' and alg != 'global':
            raise ValueError('alg must be either local or global.')

        if matrix and matrix not in _BLOSUM_MATRIX_NAMES:
            raise ValueError(f'matrix must be one of: {", ".join(_BLOSUM_MATRIX_NAMES)}')

        if threshold and threshold < 0 or threshold > 1:
            raise ValueError('threshold must be between 0 and 1.')

        if max_quantity and max_quantity < 1:
            raise ValueError('max_quantity must be at least 1.')

        return SingleAlignmentOptions(alg, matrix, threshold, max_quantity)


def replace_atypical_aas(seq: str) -> str:
    return seq.replace('O', 'K').replace('J', 'L').replace('U', 'C')


def align_single_query(database: Iterable[Peptide], query: str, options: SingleAlignmentOptions) -> List[SingleAlignedPeptide]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load(options.matrix)
    aligner.mode = options.alg

    max_score = sum([aligner.substitution_matrix[a, a] for a in query])

    result = []
    for target in database:
        score = aligner.score(replace_atypical_aas(target.sequence), query)
        score_ratio = score / float(max_score)

        if score_ratio >= options.threshold:
            result.append(SingleAlignedPeptide(target.id, target.sequence, target.length, score_ratio))

    result.sort(key=lambda n: -n.score)

    if options.max_quantity:
        result = result[0:options.max_quantity]

    return result
