import pytest

from main.utils import env_parsers


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
