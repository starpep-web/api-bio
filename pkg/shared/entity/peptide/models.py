from dataclasses import dataclass
from typing import Dict, Any, List
from pkg.shared.services.neo4j.models import Neo4jModel


@dataclass
class BasePeptide(Neo4jModel):
    id: str
    sequence: str
    length: int

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'BasePeptide':
        return BasePeptide(
            id=BasePeptide.format_id(properties['id']),
            sequence=properties['seq'],
            length=properties['length']
        )

    @staticmethod
    def format_id(identifier: int) -> str:
        return f'starPep_{identifier:05d}'


@dataclass
class PeptideMetadata(Neo4jModel):
    assessedAgainst: List[str]
    compiledIn: List[str]
    constitutedBy: List[str]
    linkedTo: List[str]
    modifiedBy: List[str]
    producedBy: List[str]
    relatedTo: List[str]

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'PeptideMetadata':
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
class SearchPeptideAttributes(Neo4jModel):
    hydropathicity: float
    charge: int
    isoelectricPoint: float
    bomanIndex: float
    gaacAlphatic: float
    gaacAromatic: float
    gaacPositiveCharge: float
    gaacNegativeCharge: float
    gaacUncharge: float

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'SearchPeptideAttributes':
        return SearchPeptideAttributes(
            hydropathicity=properties['hydropathicity'],
            charge=properties['charge'],
            isoelectricPoint=properties['isoelectric_point'],
            bomanIndex=properties['boman_index'],
            gaacAlphatic=properties['gaac_alphatic'],
            gaacAromatic=properties['gaac_aromatic'],
            gaacPositiveCharge=properties['gaac_positive_charge'],
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
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'FullPeptideAttributes':
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
class SearchPeptide(BasePeptide):
    attributes: SearchPeptideAttributes

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'SearchPeptide':
        as_base_peptide = BasePeptide.from_neo4j_properties(properties)
        attributes = SearchPeptideAttributes.from_neo4j_properties(properties['attributes'])

        return SearchPeptide(
            id=as_base_peptide.id,
            sequence=as_base_peptide.sequence,
            length=as_base_peptide.length,
            attributes=attributes
        )


@dataclass
class Peptide(BasePeptide):
    metadata: PeptideMetadata
    attributes: FullPeptideAttributes

    @staticmethod
    def from_neo4j_properties(properties: Dict[str, Any]) -> 'Peptide':
        as_base_peptide = BasePeptide.from_neo4j_properties(properties)
        metadata = PeptideMetadata.from_neo4j_properties(properties)
        attributes = FullPeptideAttributes.from_neo4j_properties(properties['attributes'])

        return Peptide(
            id=as_base_peptide.id,
            sequence=as_base_peptide.sequence,
            length=as_base_peptide.length,
            metadata=metadata,
            attributes=attributes
        )
