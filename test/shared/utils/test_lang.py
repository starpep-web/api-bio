import pkg.shared.utils.lang as module


class TestSafeAttributeChain:
    data = {
        'nested': {
            'exists': True
        },
        'exists': 'Yes',
        'list': [
            {'a': 1},
            {'a': 2}
        ]
    }

    def test_should_return_property_if_exists_simple(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['exists']) == 'Yes'

    def test_should_return_property_if_exists_nested(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['nested']['exists']) is True

    def test_should_return_property_if_exists_list(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['list'][0]['a']) is 1

    def test_should_return_none_if_not_exists_simple(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['unknown']) is None

    def test_should_return_none_if_not_exists_nested(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['nested']['unknown']) is None

    def test_should_return_none_if_not_exists_list(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['list'][0]['b']) is None
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['list'][2]['a']) is None

    def test_should_return_default_if_not_exists_simple(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['unknown'], 'default') is 'default'

    def test_should_return_default_if_not_exists_nested(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['nested']['unknown'], 'default') is 'default'

    def test_should_return_default_if_not_exists_list(self):
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['list'][0]['b'], -1) is -1
        assert module.safe_attribute_chain(lambda: TestSafeAttributeChain.data['list'][2]['a'], -1) is -1


class TestSafeJsonParse:
    obj = '''
    {
        "key": "value"
    }
    '''
    list = '''
    [0, 1, 2]
    '''
    invalid = 'invalid json'

    def test_should_return_parsed_valid_json_object(self):
        result = module.safe_json_parse(TestSafeJsonParse.obj)

        assert isinstance(result, dict) is True
        assert result['key'] == 'value'

    def test_should_return_parsed_valid_json_list(self):
        result = module.safe_json_parse(TestSafeJsonParse.list)

        assert isinstance(result, list) is True
        assert result[0] == 0

    def test_should_return_none_if_invalid(self):
        result = module.safe_json_parse(TestSafeJsonParse.invalid)
        assert result is None

    def test_should_return_default_if_invalid(self):
        result = module.safe_json_parse(TestSafeJsonParse.invalid, 'default')
        assert result is 'default'

    def test_should_return_none_if_none(self):
        result = module.safe_json_parse(None)
        assert result is None

    def test_should_return_default_if_none(self):
        result = module.safe_json_parse(None, 'default')
        assert result is 'default'


class TestSafeFloat:
    def test_should_return_valid_float(self):
        result = module.safe_float('3.14')

        assert result == 3.14

    def test_should_return_none_if_none(self):
        result = module.safe_float(None)

        assert result is None

    def test_should_return_none_if_error(self):
        result = module.safe_float('whatever')

        assert result is None


class TestSafeInt:
    def test_should_return_valid_float(self):
        result = module.safe_int('3')

        assert result == 3

    def test_should_return_none_if_none(self):
        result = module.safe_int(None)

        assert result is None

    def test_should_return_none_if_error(self):
        result = module.safe_int('whatever')

        assert result is None
