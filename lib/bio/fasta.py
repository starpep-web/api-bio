from typing import List, TextIO
from io import StringIO
from Bio import SeqIO
from Bio.Seq import Seq
from services.database.models import Peptide


def parse_fasta_string(fasta_string: str) -> List[SeqIO.SeqRecord]:
    with StringIO(fasta_string) as handler:
        parsed = SeqIO.parse(handler, format='fasta')
        return list(parsed)


def is_single_fasta_valid(fasta: List[SeqIO.SeqRecord]) -> bool:
    return len(fasta) == 1 and fasta[0].seq != ''


def build_fasta_string_from_peptide(peptide: Peptide) -> str:
    record = SeqIO.SeqRecord(id=peptide.id, seq=Seq(peptide.sequence), description='')
    return SeqIO.FastaIO.as_fasta(record)


def write_fasta_to_handler_from_peptides(handler: TextIO, peptides: List[Peptide]) -> None:
    writer = SeqIO.FastaIO.FastaWriter(handler)

    for peptide in peptides:
        record = SeqIO.SeqRecord(id=peptide.id, seq=Seq(peptide.sequence), description='')
        writer.write_record(record)


def build_fasta_string_from_peptides(peptides: List[Peptide]) -> str:
    with StringIO() as handler:
        write_fasta_to_handler_from_peptides(handler, peptides)
        return handler.getvalue()
