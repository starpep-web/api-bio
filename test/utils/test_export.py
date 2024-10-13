import pkg.utils.export as module
import pytest


class TestBase64ToBitArray:
    def test_should_throw_if_empty_string(self):
        with pytest.raises(ValueError, match='Cannot convert from empty base64 string.'):
            module.base64_to_bit_array('')

    def test_should_throw_if_invalid_string(self):
        with pytest.raises(ValueError, match='Invalid base64 string provided.'):
            module.base64_to_bit_array('__ sad')

    def test_should_parse_simple_string_no_padding(self):
        converted = module.base64_to_bit_array('aAaA')
        expected = [
            0, 1, 1, 0, 1, 0, 0, 0,
            0, 0, 0, 0, 0, 1, 1, 0,
            1, 0, 0, 0, 0, 0, 0, 0
        ]

        assert converted == expected

    def test_should_parse_simple_string_with_1_padding(self):
        converted = module.base64_to_bit_array('zMA=')
        expected = [
            1, 1, 0, 0, 1, 1, 0, 0,
            1, 1, 0, 0, 0, 0, 0, 0
        ]

        assert converted == expected

    def test_should_parse_simple_string_with_2_padding(self):
        converted = module.base64_to_bit_array('aA==')
        expected = [
            0, 1, 1, 0, 1, 0, 0, 0
        ]

        assert converted == expected

    def test_should_parse_complex_string(self):
        base64string = '/' * 7520
        converted = module.base64_to_bit_array(base64string)
        expected = [1] * 45120

        assert converted == expected
