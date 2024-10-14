from dataclasses import dataclass
from typing import Optional, Dict, Any
from pkg.shared.entity.peptide.models import SearchPeptide
from pkg.shared.entity.search.single_query.model import SingleAlignmentOptions
from pkg.shared.helpers.bio.alignment import SUPPORTED_CRITERIA, DEFAULT_CRITERION


@dataclass
class MultiAlignedPeptide(SearchPeptide):
    score: float
    avg_score: float
    max_score: float
    min_score: float


@dataclass
class MultiAlignmentOptions(SingleAlignmentOptions):
    criterion: str

    @staticmethod
    def _validate_criterion(criterion: Optional[str]) -> None:
        if criterion and criterion not in SUPPORTED_CRITERIA:
            raise ValueError(f'criterion must be one of: {", ".join(SUPPORTED_CRITERIA)}')

    @staticmethod
    def create_from_params(params: Dict[str, Any]) -> 'MultiAlignmentOptions':
        single_alignment_options = SingleAlignmentOptions.create_from_params(params)
        criterion = params.get('criterion', DEFAULT_CRITERION)

        MultiAlignmentOptions._validate_criterion(criterion)

        return MultiAlignmentOptions(**single_alignment_options.__dict__, criterion=criterion)
