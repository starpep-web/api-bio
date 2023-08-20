from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, List


_VALID_PAYLOAD_TYPES = ['text', 'single', 'multi']


@dataclass
class SearchExportForm:
    attributes: bool
    metadata: bool
    fasta: bool
    esmMean: bool
    iFeatureAac: bool
    iFeatureDpc: bool
    pdb: bool


@dataclass
class SearchExportRequestPayload:
    type: str
    form: SearchExportForm
    data: str

    def is_text(self) -> bool:
        return self.type == 'text'

    def is_single_query(self) -> bool:
        return self.type == 'single'

    def is_multi_query(self) -> bool:
        return self.type == 'multi'

    @staticmethod
    def from_json(json: Dict[str, Any]) -> SearchExportRequestPayload:
        payload_type = json.get('type', None)
        form = SearchExportForm(**json.get('form', {}))
        data = json.get('data', None)

        if not payload_type or payload_type not in _VALID_PAYLOAD_TYPES:
            raise TypeError(f'Invalid payload type, must be one of: {", ".join(_VALID_PAYLOAD_TYPES)}')

        if not any(form.__dict__.values()):
            raise TypeError('Form needs to have at least one item set to true.')

        if not data or not isinstance(data, str) or len(data) < 1:
            raise TypeError('Data needs to be a non-empty string.')

        return SearchExportRequestPayload(
            type=payload_type,
            form=form,
            data=data
        )
