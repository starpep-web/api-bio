SUPPORTED_MATRIX_NAMES = ('BLOSUM45', 'BLOSUM50', 'BLOSUM62', 'BLOSUM80', 'BLOSUM90', 'PAM30', 'PAM70', 'PAM250')
SUPPORTED_ALGORITHMS = ('global', 'local')
SUPPORTED_CRITERIA = ('avg', 'max', 'min')

DEFAULT_ALGORITHM = 'local'
DEFAULT_MATRIX_NAME = 'BLOSUM62'
DEFAULT_THRESHOLD = 1.0
DEFAULT_MAX_QUANTITY = None
DEFAULT_CRITERION = 'avg'


def replace_ambiguous_amino_acids(seq: str) -> str:
    return seq.replace('O', 'K').replace('J', 'L').replace('U', 'C')
