from typing import Iterable, List
from Bio.Align import substitution_matrices, PairwiseAligner
from pkg.shared.entity.peptide.models import SearchPeptide
from pkg.shared.entity.search.single_query.model import SingleAlignmentOptions, SingleAlignedPeptide
from pkg.shared.helpers.bio.alignment import replace_ambiguous_amino_acids


def align_single_query(database: Iterable[SearchPeptide], query: str, options: SingleAlignmentOptions) -> List[SingleAlignedPeptide]:
    aligner = PairwiseAligner()
    aligner.substitution_matrix = substitution_matrices.load(options.matrix)
    aligner.mode = options.alg

    max_score = sum([max(aligner.substitution_matrix[a]) for a in query])

    result = []
    for target in database:
        score = aligner.score(replace_ambiguous_amino_acids(target.sequence), query)
        score_ratio = round(score / float(max_score), 2)

        if score_ratio >= options.threshold:
            result.append(SingleAlignedPeptide(
                id=target.id,
                sequence=target.sequence,
                length=target.length,
                attributes=target.attributes,
                score=score_ratio
            ))

    result.sort(key=lambda n: -n.score)

    if options.max_quantity:
        result = result[0:options.max_quantity]

    return result
