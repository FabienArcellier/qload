from qload import expression

def test_jmespath_find_all_should_match_expression():
    content = {
        'foo': {'bar': 'baz'}
    }

    result = expression.jmespath_find_all(content, 'foo.bar')

    assert result == 'baz'


def test_jmespath_find_all_should_match_list():
    content = {
        'foo': [{'bar': 'baz'}, {'bar': 'baz'}]
    }

    result = expression.jmespath_find_all(content, 'foo[*].bar')

    assert result == ['baz', 'baz']


def test_jmespath_find_all_should_match_nothing():
    content = {
        'foo': [{'bar': 'baz'}, {'bar': 'baz'}]
    }

    result = expression.jmespath_find_all(content, 'foo[*].bar')

    assert result == ['baz', 'baz']


def test_jmespath_find_all_should_match_list_of_dict():
    content = {
        'foo': [{'bar': 'baz'}, {'bar': 'baz'}]
    }

    result = expression.jmespath_find_all(content, 'foo[*]')

    assert result == [{'bar': 'baz'}, {'bar': 'baz'}]


def test_re_find_all_should_find_nothing():
    content = """
    database: hello world
    """

    result = expression.re_find_all(content, 'yolo')

    assert result is None
