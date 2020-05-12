import pytest

from main.utils import env_parsers


@pytest.mark.unittest
@pytest.mark.parametrize('a_value, expected', [
    [None, AttributeError],
    ['', ['']],
    [',', ['', '']],
    ['a,b', ['a', 'b']],
    ['a, b', ['a', 'b']],
    ['a , b', ['a', 'b']],
    ['a ,b', ['a', 'b']],
    [' a , b ', ['a', 'b']],
])
def test_parse_csv_to_list(a_value, expected):
    try:
        assert env_parsers.parse_csv_to_list(a_value) == expected
    except BaseException as exception:
        with pytest.raises(expected):
            raise exception


@pytest.mark.unittest
@pytest.mark.parametrize('a_value, expected', [
    [None, AttributeError],
    ['a', 'a'],
    ['"a"', 'a'],
    ["'a'", 'a'],
    ['', ''],
    ["''a''", 'a'],
    ['""a""', 'a'],
    ['"\'a\'"', 'a'],
    ['\'"a\'"', 'a'],
])
def test_remove_closing_quotes(a_value, expected):
    try:
        assert env_parsers.remove_closing_quotes(a_value) == expected
    except BaseException as exception:
        with pytest.raises(expected):
            raise exception


@pytest.mark.unittest
@pytest.mark.parametrize('a_value, expected', [
    [None, AttributeError],
    ['true', True],
    ['True', True],
    ["TRUE", True],
    ['', False],
    ['false', False],
    ['False', False],
    ['FALSE', False],
    ['some string', False],
])
def test_parse_bool(a_value, expected):
    try:
        assert env_parsers.parse_bool(a_value) == expected
    except BaseException as exception:
        with pytest.raises(expected):
            raise exception
