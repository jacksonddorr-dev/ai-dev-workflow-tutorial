"""Small display-formatting helpers, kept separate so they're easy to test
and reuse across KPI cards."""


def format_currency(amount: float) -> str:
    """Format a dollar amount as $X,XXX,XXX, rounded to whole dollars."""
    return f"${amount:,.0f}"


def format_number(n: int) -> str:
    """Format an integer with thousands separators."""
    return f"{n:,}"
