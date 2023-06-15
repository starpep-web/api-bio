from __future__ import annotations
from typing import Iterable, Optional, Dict, Any, List
from dataclasses import dataclass
from Bio.Align import substitution_matrices, PairwiseAligner
from services.database.models import Peptide


# TODO: Implement multi alignment
_SUPPORTED_MATRIX_NAMES = ('BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM30', 'PAM70', 'PAM250')
_SUPPORTED_ALGORITHMS = ('global', 'local')

_DEFAULT_ALGORITHM = 'local'
_DEFAULT_MATRIX_NAME = 'BLOSUM62'
_DEFAULT_THRESHOLD = 1.0
_DEFAULT_MAX_QUANTITY = None


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
    def _validate_alg(alg: Optional[str]) -> None:
        if alg and alg not in _SUPPORTED_ALGORITHMS:
            raise ValueError(f'alg must be one of: {", ".join(_SUPPORTED_ALGORITHMS)}')

    @staticmethod
    def _validate_matrix(matrix: Optional[str]) -> None:
        if matrix and matrix not in _SUPPORTED_MATRIX_NAMES:
            raise ValueError(f'matrix must be one of: {", ".join(_SUPPORTED_MATRIX_NAMES)}')

    @staticmethod
    def _validate_threshold(threshold: Optional[float]) -> None:
        if threshold and not 0 < threshold <= 1.0:
            raise ValueError('threshold must be between 0 and 1.')

    @staticmethod
    def _validate_max_quantity(max_quantity: Optional[int]) -> None:
        if max_quantity and not max_quantity > 0:
            raise ValueError('max_quantity must be at least 1.')

    @staticmethod
    def create_from_params(params: Dict[str, Any]) -> SingleAlignmentOptions:
        alg = params.get('alg', _DEFAULT_MATRIX_NAME)
        matrix = params.get('matrix', _DEFAULT_MATRIX_NAME)
        threshold = params.get('threshold', None)
        threshold = float(threshold) if threshold else _DEFAULT_THRESHOLD
        max_quantity = params.get('max_quantity', None)
        max_quantity = int(max_quantity) if max_quantity else _DEFAULT_MAX_QUANTITY

        SingleAlignmentOptions._validate_alg(alg)
        SingleAlignmentOptions._validate_matrix(matrix)
        SingleAlignmentOptions._validate_threshold(threshold)
        SingleAlignmentOptions._validate_max_quantity(max_quantity)

        return SingleAlignmentOptions(alg, matrix, threshold, max_quantity)


def replace_ambiguous_amino_acids(seq: str) -> str:
    return seq.replace('O', 'K').replace('J', 'L').replace('U', 'C')


def align_single_query(database: Iterable[Peptide], query: str, options: SingleAlignmentOptions) -> List[SingleAlignedPeptide]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load(options.matrix)
    aligner.mode = options.alg

    max_score = sum([aligner.substitution_matrix[a, a] for a in query])

    result = []
    for target in database:
        score = aligner.score(replace_ambiguous_amino_acids(target.sequence), query)
        score_ratio = score / float(max_score)

        if score_ratio >= options.threshold:
            result.append(SingleAlignedPeptide(target.id, target.sequence, target.length, score_ratio))

    result.sort(key=lambda n: -n.score)

    if options.max_quantity:
        result = result[0:options.max_quantity]

    return result
