from formatting import format_currency, format_number


def test_format_currency_adds_dollar_sign_and_separators():
    assert format_currency(116543.21) == "$116,543"


def test_format_currency_rounds_to_whole_dollars():
    assert format_currency(99.6) == "$100"


def test_format_number_adds_thousands_separators():
    assert format_number(482) == "482"
    assert format_number(1234567) == "1,234,567"
