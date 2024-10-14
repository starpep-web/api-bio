from typing import Iterable, List
from statistics import mean
from Bio.Align import substitution_matrices, PairwiseAligner
from pkg.shared.entity.peptide.models import SearchPeptide
from pkg.shared.entity.search.multi_query.model import MultiAlignmentOptions, MultiAlignedPeptide
from pkg.shared.helpers.bio.alignment import replace_ambiguous_amino_acids


def align_multi_query(database: Iterable[SearchPeptide], queries: List[str], options: MultiAlignmentOptions) -> List[MultiAlignedPeptide]:
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
