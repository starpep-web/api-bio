from typing import List
from base64 import b64decode
import binascii


def base64to_bit_array(base64string: str) -> List[int]:
    if not len(base64string):
        raise ValueError('Cannot convert from empty base64 string.')

    try:
        decoded_bytes = b64decode(base64string, validate=True)
    except binascii.Error:
        raise ValueError('Invalid base64 string provided.')

    bit_array = []
    for byte in decoded_bytes:
        binary = format(byte, '08b')
        bit_array_for_byte = [1 if c == '1' else 0 for c in binary]

        bit_array += bit_array_for_byte

    return bit_array
