from typing import List
from Bio import SeqIO
from services.database.models import Peptide
from lib.bio.alignment import blosum_align_query, replace_atypical_aas, AlignmentOptions, AlignedPeptide


def run_single_query(peptide_database: List[Peptide], query_record: SeqIO.SeqRecord, options: AlignmentOptions) -> List[AlignedPeptide]:
    fixed_query = replace_atypical_aas(query_record.seq)
    return blosum_align_query(peptide_database, fixed_query, options)
