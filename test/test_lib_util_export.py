import unittest
from lib.utils.export import base64to_bit_array


class TestBase64ToBitArray(unittest.TestCase):
    def test_throw_if_empty_string(self):
        """
        It should throw if attempting to parse an empty string.
        """

        with self.assertRaises(ValueError):
            base64to_bit_array('')

    def test_throw_if_invalid_string(self):
        """
        It should throw if attempting to parse an invalid base64 string.
        """

        with self.assertRaises(ValueError):
            base64to_bit_array('àà')

    def test_simple_convert_no_padding(self):
        """
        It should return an array of bits corresponding to a simple base64 string with no padding.
        """

        converted = base64to_bit_array('aAaA')
        expected = [
            0, 1, 1, 0, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 0, 0, 0, 0, 0, 0
        ]

        self.assertListEqual(converted, expected)

    def test_simple_convert_padding_1(self):
        """
        It should return an array of bits corresponding to a simple base64 string with 1 padding character.
        """

        converted = base64to_bit_array('zMA=')
        expected = [
            1, 1, 0, 0, 1, 1, 0, 0,
            1, 1, 0, 0, 0, 0, 0, 0
        ]

        self.assertListEqual(converted, expected)

    def test_simple_convert_padding_2(self):
        """
        It should return an array of bits corresponding to a simple base64 string with 2 padding characters.
        """

        converted = base64to_bit_array('aA==')
        expected = [
            0, 1, 1, 0, 1, 0, 0, 0
        ]

        self.assertListEqual(converted, expected)

    def test_complex_convert(self):
        """
        It should return an array of bits corresponding to a complex base64 string.
        """

        base64string = '/' * 7520
        converted = base64to_bit_array(base64string)
        expected = [1] * 45120

        self.assertListEqual(converted, expected)


if __name__ == '__main__':
    unittest.main()
