def remove_closing_quotes(quoted_string: str) -> str:
    def has_closing_quotes(quoted_string):
        _quotes = ['"', "'"]
        does_starts = any(quoted_string.startswith(quote) for quote in _quotes)
        does_ends = any(quoted_string.endswith(quote) for quote in _quotes)
        return does_starts or does_ends

    while has_closing_quotes(quoted_string):
        quoted_string = quoted_string.strip('"').strip("'")
    return quoted_string
