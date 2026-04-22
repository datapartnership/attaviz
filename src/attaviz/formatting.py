"""Number and date formatting utilities following WBG style guide.

Provides both Python formatting functions for data preprocessing and D3 format
strings for use in Altair axis/tooltip labels.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Literal, Union

# Scale thresholds and suffixes
_SCALES = [
    (1_000_000_000, "B"),
    (1_000_000, "M"),
    (1_000, "K"),
]

# Units that use G instead of B (watts, tons, bits, bytes)
_G_UNITS = {"W", "watt", "watts", "ton", "tons", "bit", "bits", "byte", "bytes"}

ScaleType = Literal["K", "M", "B", "G", "auto"]
DateStyle = Literal["day", "month", "month_year", "quarter", "year", "fiscal_year"]


def format_number(
    value: float | int,
    *,
    decimals: int | Literal["auto"] = "auto",
    scale: ScaleType = "auto",
    currency: bool = False,
    percent: bool = False,
    unit: str | None = None,
) -> str:
    """Format a number according to WBG style guide.

    Parameters
    ----------
    value
        The number to format.
    decimals
        Number of decimal places. If "auto", uses WBG rules:
        2 decimals for |v| < 1, 1 decimal for 1-100, 0 for > 100.
    scale
        Scale suffix: "K" (thousands), "M" (millions), "B" (billions),
        "G" (giga, for technical units), or "auto" for automatic scaling.
    currency
        If True, prefix with "$".
    percent
        If True, multiply by 100 and suffix with "%".
    unit
        Optional unit name. If in ["W", "watt", "tons", "bit", "byte", ...],
        uses "G" instead of "B" for billions.

    Returns
    -------
    str
        The formatted number string.

    Examples
    --------
    >>> format_number(1234567)
    '1.2M'
    >>> format_number(0.456, percent=True)
    '45.60%'
    >>> format_number(1234567890, unit="bytes")
    '1.2G'
    >>> format_number(50000, currency=True)
    '$50K'
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"

    if percent:
        value = value * 100

    abs_value = abs(value)

    scale_factor = 1
    scale_suffix = ""

    if scale == "auto" and not percent:
        for threshold, suffix in _SCALES:
            if abs_value >= threshold:
                scale_factor = threshold
                scale_suffix = suffix
                if (
                    suffix == "B"
                    and unit
                    and unit.lower().rstrip("s")
                    in {u.lower().rstrip("s") for u in _G_UNITS}
                ):
                    scale_suffix = "G"
                break
    elif scale in ("K", "M", "B", "G"):
        scale_map = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000, "G": 1_000_000_000}
        scale_factor = scale_map[scale]
        scale_suffix = scale

    scaled_value = value / scale_factor

    if decimals == "auto":
        abs_scaled = abs(scaled_value)
        if abs_scaled < 1:
            dec = 2
        elif abs_scaled < 100:
            dec = 1
        else:
            dec = 0
    else:
        dec = decimals

    formatted = f"{scaled_value:,.{dec}f}"

    prefix = "$" if currency else ""
    suffix = "%" if percent else scale_suffix

    return f"{prefix}{formatted}{suffix}"


def d3_number_format(
    scale: Literal["K", "M", "B", "G"] | None = None,
    decimals: int = 1,
    currency: bool = False,
    percent: bool = False,
) -> str:
    """Return a D3 format string for Altair axis/tooltip labels.

    Note: D3 format strings don't support automatic scaling with custom suffixes.
    For scaled values (K/M/B), the user should:
    1. Pre-scale the data, or
    2. Add the suffix via axis title (e.g., "GDP (millions)")

    Parameters
    ----------
    scale
        Not used for D3 format (included for API consistency).
        Scale should be indicated in axis title instead.
    decimals
        Number of decimal places.
    currency
        If True, prefix with "$".
    percent
        If True, format as percentage.

    Returns
    -------
    str
        A D3 format string.

    Examples
    --------
    >>> d3_number_format()
    ',.1f'
    >>> d3_number_format(decimals=0)
    ',.0f'
    >>> d3_number_format(currency=True)
    '$,.1f'
    >>> d3_number_format(percent=True)
    '.1%'
    """
    if percent:
        return f".{decimals}%"

    prefix = "$" if currency else ""
    return f"{prefix},.{decimals}f"


def vega_scale_labelExpr(
    *,
    currency: bool = False,
    unit: str | None = None,
    decimals: int = 1,
) -> str:
    """Return a Vega expression string for auto-scaled Altair axis labels.

    Unlike ``d3_number_format``, this produces a *Vega expression* (for use
    with ``alt.Axis(labelExpr=...)``) that applies WBG-style K/M/B suffixes
    per-tick in the browser — no data pre-scaling required.

    Parameters
    ----------
    currency
        If True, prefix every label with "$".
    unit
        If provided and the unit is a technical one (W, ton, bit, byte, ...),
        the billions suffix becomes "G" instead of "B".
    decimals
        Decimal places for the scaled value. Defaults to 1 (WBG default for
        the 1-100 range, which covers most scaled ticks).

    Returns
    -------
    str
        A Vega expression string suitable for ``alt.Axis(labelExpr=...)``.

    Examples
    --------
    >>> import altair as alt  # doctest: +SKIP
    >>> axis = alt.Axis(labelExpr=vega_scale_labelExpr(currency=True))
    """
    prefix = "$" if currency else ""

    # Swap "B" -> "G" for technical units, matching format_number's behavior.
    billions_suffix = "B"
    if unit and unit.lower().rstrip("s") in {u.lower().rstrip("s") for u in _G_UNITS}:
        billions_suffix = "G"

    spec = f"',.{decimals}f'"
    int_spec = "',.0f'"
    v = "datum.value"
    p = repr(prefix)

    return (
        f"abs({v}) >= 1e9 ? {p} + format({v}/1e9, {spec}) + '{billions_suffix}' : "
        f"abs({v}) >= 1e6 ? {p} + format({v}/1e6, {spec}) + 'M' : "
        f"abs({v}) >= 1e3 ? {p} + format({v}/1e3, {spec}) + 'K' : "
        f"{p} + format({v}, {int_spec})"
    )


def format_date(
    value: Union[date, datetime, str],
    style: DateStyle = "month_year",
    short: bool = True,
) -> str:
    """Format a date according to WBG style guide.

    Parameters
    ----------
    value
        The date to format. Can be a date, datetime, or ISO string.
    style
        The format style:
        - "day": Full date (e.g., "1/15/2023" or "January 15, 2023")
        - "month": Month only (e.g., "Jan" or "January")
        - "month_year": Month and year (e.g., "Jan-23" or "January 2023")
        - "quarter": Quarter format (e.g., "Q1-23" or "Q1 2023")
        - "year": Year only (e.g., "23" or "2023")
        - "fiscal_year": Fiscal year (e.g., "FY23" or "FY2023")
    short
        If True, use abbreviated format.

    Returns
    -------
    str
        The formatted date string.

    Examples
    --------
    >>> from datetime import date
    >>> format_date(date(2023, 1, 15), style="month_year")
    'Jan-23'
    >>> format_date(date(2023, 1, 15), style="month_year", short=False)
    'January 2023'
    >>> format_date(date(2023, 3, 1), style="quarter")
    'Q1-23'
    """
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(value, datetime):
        value = value.date()

    if style == "day":
        if short:
            return value.strftime("%-m/%-d/%Y")
        return value.strftime("%B %-d, %Y")

    if style == "month":
        if short:
            return value.strftime("%b")
        return value.strftime("%B")

    if style == "month_year":
        if short:
            return value.strftime("%b-%y")
        return value.strftime("%B %Y")

    if style == "quarter":
        quarter = (value.month - 1) // 3 + 1
        if short:
            return f"Q{quarter}-{value.strftime('%y')}"
        return f"Q{quarter} {value.year}"

    if style == "year":
        if short:
            return value.strftime("%y")
        return value.strftime("%Y")

    if style == "fiscal_year":
        # WBG fiscal year runs July-June. July 2023 is FY24; Jan 2023 is FY23.
        fy = value.year + 1 if value.month >= 7 else value.year
        if short:
            return f"FY{fy % 100:02d}"
        return f"FY{fy}"

    raise ValueError(f"Unknown date style: {style}")


def d3_date_format(
    style: DateStyle = "month_year",
    short: bool = True,
) -> str:
    """Return a D3 time format string for Altair temporal axes.

    Parameters
    ----------
    style
        The format style (see format_date for descriptions).
    short
        If True, use abbreviated format.

    Returns
    -------
    str
        A D3 time format string.

    Examples
    --------
    >>> d3_date_format("month_year")
    '%b-%y'
    >>> d3_date_format("month_year", short=False)
    '%B %Y'
    >>> d3_date_format("year")
    '%y'

    Notes
    -----
    The "quarter" and "fiscal_year" styles cannot be represented as D3 time
    format strings. For those, compute the formatted value in Python via
    ``format_date`` and pass the resulting string to Altair, or use a Vega
    expression in the axis encoding.
    """
    formats = {
        "day": ("%m/%d/%Y", "%B %d, %Y"),
        "month": ("%b", "%B"),
        "month_year": ("%b-%y", "%B %Y"),
        "year": ("%y", "%Y"),
    }

    if style in ("quarter", "fiscal_year"):
        raise ValueError(
            f"Style '{style}' has no D3 time-format equivalent. "
            "Use format_date() to preformat values, or supply a Vega expression."
        )
    if style not in formats:
        raise ValueError(f"Unknown date style: {style}")

    short_fmt, long_fmt = formats[style]
    return short_fmt if short else long_fmt
