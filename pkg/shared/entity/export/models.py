from dataclasses import dataclass
from typing import Any, List, Dict
from pydantic import BaseModel, field_validator


_VALID_PAYLOAD_TYPES = ['text', 'single', 'multi']


class SearchExportForm(BaseModel):
    attributes: bool = False
    metadata: bool = False
    fasta: bool = False
    esmMean: bool = False
    iFeatureAac: bool = False
    iFeatureDpc: bool = False
    pdb: bool = False

    def get_exportable_resources(self) -> List[str]:
        return [k for k, v in self.__dict__.items() if v]


class SearchExportRequestPayload(BaseModel):
    type: str
    form: SearchExportForm
    data: str

    def is_text(self) -> bool:
        return self.type == 'text'

    def is_single_query(self) -> bool:
        return self.type == 'single'

    def is_multi_query(self) -> bool:
        return self.type == 'multi'

    @field_validator('type')
    def _validate_type(cls, payload_type: Any) -> str:
        if payload_type is None or not isinstance(payload_type, str) or payload_type not in _VALID_PAYLOAD_TYPES:
            raise ValueError(f'Invalid payload type, must be one of: {", ".join(_VALID_PAYLOAD_TYPES)}')

        return payload_type

    @field_validator('form')
    def _validate_form(cls, form: Any) -> SearchExportForm:
        if form is None or not isinstance(form, SearchExportForm) or len(form.get_exportable_resources()) < 1:
            raise ValueError('Form needs to have at least one resource set to true.')

        return form

    @field_validator('data')
    def _validate_data(cls, data: Any) -> str:
        if data is None or not isinstance(data, str) or len(data) < 1:
            raise ValueError('Data needs to be a non-empty string.')

        return data


@dataclass
class SearchExportResult:
    peptideIds: List[str]
    total: int
    form: SearchExportForm
    done: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {'peptideIds': self.peptideIds, 'total': self.total, 'form': self.form.model_dump(), 'done': self.done}
