from __future__ import annotations
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Model(ABC):
    @staticmethod
    @abstractmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> Model:
        pass


@dataclass
class Peptide(Model):
    id: str
    sequence: str
    length: int

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> Peptide:
        return Peptide(
            id=Peptide.format_id(properties['id']),
            sequence=properties['seq'],
            length=properties['length']
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
    def from_neo4j_properties(properties: Dict[str, Any]) -> PeptideMetadata:
        return PeptideMetadata(
            assessedAgainst=properties.get('assessed_against', []),
            compiledIn=properties.get('compiled_in', []),
            constitutedBy=properties.get('constituted_by', []),
            linkedTo=properties.get('linked_to', []),
            modifiedBy=properties.get('modified_by', []),
            producedBy=properties.get('produced_by', []),
            relatedTo=properties.get('related_to', [])
        )


@dataclass
class SearchPeptideAttributes(Model):
    hydropathicity: float
    charge: int
    isoelectricPoint: float
    bomanIndex: float
    gaacAlphatic: float
    gaacAromatic: float
    gaacPostiveCharge: float
    gaacNegativeCharge: float
    gaacUncharge: float

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> SearchPeptideAttributes:
        return SearchPeptideAttributes(
            hydropathicity=properties['hydropathicity'],
            charge=properties['charge'],
            isoelectricPoint=properties['isoelectric_point'],
            bomanIndex=properties['boman_index'],
            gaacAlphatic=properties['gaac_alphatic'],
            gaacAromatic=properties['gaac_aromatic'],
            gaacPostiveCharge=properties['gaac_postive_charge'],
            gaacNegativeCharge=properties['gaac_negative_charge'],
            gaacUncharge=properties['gaac_uncharge']
        )


@dataclass
class FullPeptideAttributes(SearchPeptideAttributes):
    hydrophobicity: float
    solvation: float
    amphiphilicity: float
    hydrophilicity: float
    hemolyticProbScore: float
    stericHindrance: float
    netHydrogen: int
    molWt: float
    aliphaticIndex: float

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> FullPeptideAttributes:
        search_attributes = SearchPeptideAttributes.from_neo4j_properties(properties)

        return FullPeptideAttributes(
            hydrophobicity=properties['hydrophobicity'],
            solvation=properties['solvation'],
            amphiphilicity=properties['amphiphilicity'],
            hydrophilicity=properties['hydrophilicity'],
            hemolyticProbScore=properties['hemolytic_prob_score'],
            stericHindrance=properties['steric_hindrance'],
            netHydrogen=properties['net_hydrogen'],
            molWt=properties['mol_wt'],
            aliphaticIndex=properties['aliphatic_index'],
            **search_attributes.__dict__
        )


@dataclass
class SearchResultPeptide(Peptide):
    attributes: SearchPeptideAttributes

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> SearchResultPeptide:
        as_peptide = Peptide.from_neo4j_properties(properties)
        attributes = SearchPeptideAttributes.from_neo4j_properties(properties['attributes'])

        return SearchResultPeptide(
            id=as_peptide.id,
            sequence=as_peptide.sequence,
            length=as_peptide.length,
            attributes=attributes
        )


@dataclass
class FullPeptide(Peptide):
    metadata: PeptideMetadata
    attributes: FullPeptideAttributes

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> FullPeptide:
        as_peptide = Peptide.from_neo4j_properties(properties)
        metadata = PeptideMetadata.from_neo4j_properties(properties)
        attributes = FullPeptideAttributes.from_neo4j_properties(properties['attributes'])

        return FullPeptide(
            id=as_peptide.id,
            sequence=as_peptide.sequence,
            length=as_peptide.length,
            metadata=metadata,
            attributes=attributes
        )
