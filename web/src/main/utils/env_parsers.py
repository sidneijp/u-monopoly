from typing import List


def parse_csv_to_list(csv_string: str) -> List[str]:
    return [value.strip() for value in csv_string.split(',')]


def remove_closing_quotes(quoted_string: str) -> str:
    def has_closing_quotes(quoted_string):
        _quotes = ['"', "'"]
        does_starts = any(quoted_string.startswith(quote) for quote in _quotes)
        does_ends = any(quoted_string.endswith(quote) for quote in _quotes)
        return does_starts or does_ends

    while has_closing_quotes(quoted_string):
        quoted_string = quoted_string.strip('"').strip("'")
    return quoted_string


def parse_bool(boolean_string: str) -> bool:
    return boolean_string.lower() == 'true'
