from dataclasses import dataclass
from typing import Optional, Dict, Any
from pkg.shared.entity.peptide.models import SearchPeptide
from pkg.shared.helpers.bio.alignment import SUPPORTED_ALGORITHMS, SUPPORTED_MATRIX_NAMES, DEFAULT_MATRIX_NAME, \
    DEFAULT_ALGORITHM, DEFAULT_THRESHOLD, DEFAULT_MAX_QUANTITY


@dataclass
class SingleAlignedPeptide(SearchPeptide):
    score: float


@dataclass
class SingleAlignmentOptions:
    alg: str
    matrix: str
    threshold: float
    max_quantity: Optional[int]

    @staticmethod
    def _validate_alg(alg: Optional[str]) -> None:
        if alg and alg not in SUPPORTED_ALGORITHMS:
            raise ValueError(f'alg must be one of: {", ".join(SUPPORTED_ALGORITHMS)}')

    @staticmethod
    def _validate_matrix(matrix: Optional[str]) -> None:
        if matrix and matrix not in SUPPORTED_MATRIX_NAMES:
            raise ValueError(f'matrix must be one of: {", ".join(SUPPORTED_MATRIX_NAMES)}')

    @staticmethod
    def _validate_threshold(threshold: Optional[float]) -> None:
        if threshold and not 0 < threshold <= 1.0:
            raise ValueError('threshold must be between 0 and 1.')

    @staticmethod
    def _validate_max_quantity(max_quantity: Optional[int]) -> None:
        if max_quantity and not max_quantity > 0:
            raise ValueError('max_quantity must be at least 1.')

    @staticmethod
    def create_from_params(params: Dict[str, Any]) -> 'SingleAlignmentOptions':
        alg = params.get('alg', DEFAULT_ALGORITHM)
        matrix = params.get('matrix', DEFAULT_MATRIX_NAME)
        threshold = params.get('threshold', DEFAULT_THRESHOLD)
        threshold = float(threshold) if threshold else DEFAULT_THRESHOLD
        max_quantity = params.get('max_quantity', DEFAULT_MAX_QUANTITY)
        max_quantity = int(max_quantity) if max_quantity else DEFAULT_MAX_QUANTITY

        SingleAlignmentOptions._validate_alg(alg)
        SingleAlignmentOptions._validate_matrix(matrix)
        SingleAlignmentOptions._validate_threshold(threshold)
        SingleAlignmentOptions._validate_max_quantity(max_quantity)

        return SingleAlignmentOptions(alg, matrix, threshold, max_quantity)
