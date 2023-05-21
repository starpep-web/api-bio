from __future__ import annotations
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Model(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(dictionary: Dict[str, Any]) -> Model:
        pass


@dataclass
class Peptide(Model):
    id: str
    sequence: str
    length: int

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]) -> Peptide:
        return Peptide(
            id=Peptide.format_id(dictionary['id']),
            sequence=dictionary['seq'],
            length=dictionary['length']
        )

    @staticmethod
    def format_id(identifier: str) -> str:
        return f'starPep_{identifier:05d}'


@dataclass
class PeptideMetadata(Model):
    assessedAgainst: List[str]
    compiledIn: List[str]
    constitutedBy: List[str]
    linkedTo: List[str]
    modifiedBy: List[str]
    producedBy: List[str]
    relatedTo: List[str]

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]) -> PeptideMetadata:
        return PeptideMetadata(
            assessedAgainst=dictionary.get('assessed_against', []),
            compiledIn=dictionary.get('compiled_in', []),
            constitutedBy=dictionary.get('constituted_by', []),
            linkedTo=dictionary.get('linked_to', []),
            modifiedBy=dictionary.get('modified_by', []),
            producedBy=dictionary.get('produced_by', []),
            relatedTo=dictionary.get('related_to', [])
        )


@dataclass
class FullPeptide(Peptide):
    metadata: PeptideMetadata

    @staticmethod
    def from_dict(dictionary: Dict[str, Any]) -> FullPeptide:
        as_peptide = Peptide.from_dict(dictionary)
        metadata = PeptideMetadata.from_dict(dictionary)

        return FullPeptide(
            id=as_peptide.id,
            sequence=as_peptide.sequence,
            length=as_peptide.length,
            metadata=metadata
        )
