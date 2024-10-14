from __future__ import annotations
from typing import Iterable, Optional, Dict, Any, List
from dataclasses import dataclass
from statistics import mean
from Bio.Align import substitution_matrices, PairwiseAligner
from services.database.models import SearchResultPeptide


@dataclass
class MultiAlignedPeptide(SearchResultPeptide):
    score: float
    avg_score: float
    max_score: float
    min_score: float


@dataclass
class MultiAlignmentOptions(SingleAlignmentOptions):
    criterion: str

    @staticmethod
    def _validate_criterion(criterion: Optional[str]) -> None:
        if criterion and criterion not in _SUPPORTED_CRITERIA:
            raise ValueError(f'criterion must be one of: {", ".join(_SUPPORTED_CRITERIA)}')

    @staticmethod
    def create_from_params(params: Dict[str, Any]) -> MultiAlignmentOptions:
        single_alignment_options = SingleAlignmentOptions.create_from_params(params)
        criterion = params.get('criterion', _DEFAULT_CRITERION)

        MultiAlignmentOptions._validate_criterion(criterion)

        return MultiAlignmentOptions(**single_alignment_options.__dict__, criterion=criterion)


def align_multi_query(database: Iterable[SearchResultPeptide], queries: List[str], options: MultiAlignmentOptions) -> List[MultiAlignedPeptide]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load(options.matrix)
    aligner.mode = options.alg

    result = []
    for target in database:
        scores_for_target = []

        for query in queries:
            max_score = sum([max(aligner.substitution_matrix[a]) for a in query])
            score = aligner.score(replace_ambiguous_amino_acids(target.sequence), query)
            score_ratio = round(score / float(max_score), 2)

            scores_for_target.append(score_ratio)

        score_avg = round(mean(scores_for_target), 2)
        score_max = round(max(scores_for_target), 2)
        score_min = round(min(scores_for_target), 2)

        if options.criterion == 'avg':
            real_score = score_avg
        elif options.criterion == 'max':
            real_score = score_max
        elif options.criterion == 'min':
            real_score = score_min
        else:
            real_score = 0

        if real_score >= options.threshold:
            result.append(MultiAlignedPeptide(
                id=target.id,
                sequence=target.sequence,
                length=target.length,
                attributes=target.attributes,
                score=real_score,
                avg_score=score_avg,
                max_score=score_max,
                min_score=score_min
            ))

    result.sort(key=lambda n: -n.score)

    if options.max_quantity:
        result = result[0:options.max_quantity]

    return result
