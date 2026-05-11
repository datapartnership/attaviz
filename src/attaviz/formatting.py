"""Number and date formatting utilities following WBG style guide.

Provides both Python formatting functions for data preprocessing and D3 format
strings for use in Altair axis/tooltip labels.
"""

from __future__ import annotations

import math
from datetime import date, datetime
from typing import Literal, Union

# (min_value_to_trigger, divisor, suffix). Per WBG style guide, scaling
# kicks in at >=10,000 and below that we display the unscaled number.
_SCALES = [
    (1_000_000_000, 1_000_000_000, "B"),
    (1_000_000, 1_000_000, "M"),
    (10_000, 1_000, "K"),
]

_G_UNITS = {"W", "watt", "watts", "ton", "tons", "bit", "bits", "byte", "bytes"}

_UNIT_ABBREVS: dict[str, str] = {
    "watt": "w",
    "byte": "B",
    "bit": "b",
    "ton": "t",
}


def _normalize_unit(unit: str) -> str:
    return unit.lower().rstrip("s")


def _unit_suffix(unit: str | None) -> str:
    """Return the suffix to append after the scale letter, or '' if none."""
    if not unit:
        return ""
    key = _normalize_unit(unit)
    if key in _UNIT_ABBREVS:
        return _UNIT_ABBREVS[key]
    return f" {unit}"

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
    >>> format_number(1234)
    '1,234'
    >>> format_number(0.456, percent=True)
    '45.6%'
    >>> format_number(1234567, unit="watts")  # requires _UNIT_ABBREVS entry
    '1.2Mw'
    >>> format_number(50000, currency=True)
    '$50.0K'
    """
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "N/A"

    if value == 0 and decimals == "auto" and not percent:
        prefix = "$" if currency else ""
        return f"{prefix}0{_unit_suffix(unit)}"

    if percent:
        value = value * 100

    abs_value = abs(value)

    scale_factor = 1
    scale_suffix = ""

    g_unit_keys = {_normalize_unit(u) for u in _G_UNITS}
    is_g_unit = unit is not None and _normalize_unit(unit) in g_unit_keys

    if scale == "auto" and not percent:
        for threshold, divisor, suffix in _SCALES:
            if abs_value >= threshold:
                scale_factor = divisor
                scale_suffix = "G" if suffix == "B" and is_g_unit else suffix
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
    if percent:
        suffix = "%"
    else:
        suffix = scale_suffix + _unit_suffix(unit)

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
    decimals: int | Literal["auto"] = "auto",
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
        the billions suffix becomes "G" instead of "B". If the unit has an
        entry in ``_UNIT_ABBREVS``, that abbreviation is appended to every tick
        (e.g. "MB", "Gw").
    decimals
        Decimal places for the scaled value. "auto" (default) follows the WBG
        rule per-tick based on the *scaled* magnitude: 0 decimals if >=100,
        1 decimal if >=1, 2 decimals otherwise. Pass an int to force a fixed
        decimal count across all ticks.

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

    billions_suffix = "B"
    if unit and _normalize_unit(unit) in {_normalize_unit(u) for u in _G_UNITS}:
        billions_suffix = "G"
    unit_tail = _unit_suffix(unit)

    v = "datum.value"
    p = repr(prefix)

    def tier(scaled: str, suffix: str) -> str:
        tail = repr(suffix + unit_tail)
        if decimals == "auto":
            return (
                f"(abs({scaled}) >= 100 ? {p} + format({scaled}, ',.0f') + {tail} : "
                f"abs({scaled}) >= 1 ? {p} + format({scaled}, ',.1f') + {tail} : "
                f"{p} + format({scaled}, ',.2f') + {tail})"
            )
        spec = f"',.{decimals}f'"
        return f"({p} + format({scaled}, {spec}) + {tail})"

    zero_label = repr(prefix + "0" + unit_tail)
    return (
        f"{v} === 0 ? {zero_label} : "
        f"abs({v}) >= 1e9 ? {tier(f'{v}/1e9', billions_suffix)} : "
        f"abs({v}) >= 1e6 ? {tier(f'{v}/1e6', 'M')} : "
        f"abs({v}) >= 1e4 ? {tier(f'{v}/1e3', 'K')} : "
        f"{tier(v, '')}"
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
    '23Q1'
    """
    if isinstance(value, str):
        value = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if isinstance(value, datetime):
        value = value.date()

    if style == "day":
        if short:
            return value.strftime("%-d/%-m/%Y")
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
            return f"{value.strftime('%y')}Q{quarter}"
        return f"{value.year}Q{quarter}"

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
