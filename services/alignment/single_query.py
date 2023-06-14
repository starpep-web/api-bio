from typing import List
from Bio import SeqIO
from database.models import Peptide
from lib.bio.alignment import blosum_align_query, replace_atypical_aas


def run_single_query(peptide_database: List[Peptide], query_record: SeqIO.SeqRecord):
    fixed_query = replace_atypical_aas(query_record.seq)
    return blosum_align_query('BLOSUM62', peptide_database, fixed_query)
