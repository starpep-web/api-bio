from typing import Tuple
import os
import subprocess


_USEARCH_BIN = os.path.join(os.getenv("BIN_LOCATION"), 'usearch11.0.667_i86linux32')


# TODO: Implement Usearch in the future.

def usearch_align_local(fasta_input_filename: str) -> Tuple[str, subprocess.CompletedProcess]:
    output_filename = f'{fasta_input_filename}.aln'

    return output_filename, subprocess.run([
        _USEARCH_BIN,
        '-pairs_local', fasta_input_filename,
        '-evalue', '1e-9',
        '-alnout', output_filename
    ], shell=False, capture_output=False, text=False)


def ublast_align(fasta_query_filename: str, fasta_database_filename: str) -> Tuple[str, subprocess.CompletedProcess]:
    output_filename = f'{fasta_query_filename}.aln'

    return output_filename, subprocess.run([
        _USEARCH_BIN,
        '-ublast', fasta_query_filename,
        '-db', fasta_database_filename,
        '-evalue', '1e-6',
        '-accel', '0.5',
        '-alnout', output_filename
    ], shell=False, capture_output=False, text=False)
