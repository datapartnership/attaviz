"""World Bank Group data visualization theme for Altair.

Usage::

    import altair as alt
    import attaviz

    attaviz.enable()

    # Now all charts use the WBG theme
    chart = alt.Chart(...).mark_bar().encode(...)

    # Use size-specific themes
    attaviz.enable(size='large')

    # Per-chart sizing
    chart = attaviz.configure_size(chart, width=400, aspect_ratio='16:9')

    # Calculate dimensions
    w, h = attaviz.calculate_dimensions(800, '16:9')  # (800, 450)
"""

from __future__ import annotations

from typing import Literal

import altair as alt

from .formatting import (  # noqa: F401
    d3_date_format,
    d3_number_format,
    format_date,
    format_number,
    vega_scale_labelExpr,
)
from .colors import (  # noqa: F401
    AGE,
    BINARY,
    CATEGORICAL,
    CATEGORICAL_TEXT,
    DIV_ALTERNATIVE,
    DIV_DEFAULT,
    DIV_NEUTRAL,
    GENDER,
    GREY_100,
    GREY_200,
    GREY_300,
    GREY_400,
    GREY_500,
    INCOME,
    INCOME_LIST,
    NO_DATA,
    PILLARS,
    REFERENCE,
    REGIONS,
    REGIONS_SECONDARY,
    REGIONS_TEXT,
    SELECTION_PRIMARY,
    SELECTION_SECONDARY,
    SEQ_BAD_TO_GOOD,
    SEQ_BLUE,
    SEQ_GOOD_TO_BAD,
    SEQ_GREEN,
    SEQ_PURPLE,
    SEQ_RED,
    SEQ_YELLOW,
    TEXT,
    TEXT_SUBTLE,
    TOTAL,
    URBANIZATION,
)
from .theme import (  # noqa: F401 – re-exported as public API
    ASPECT_RATIOS,
    DEFAULT_DIMENSIONS,
    FONT,
    LINE_HEIGHT_LONG,
    SIZE_BREAKPOINTS,
    SPACING,
    TYPOGRAPHY,
    _get_size_category,
    calculate_dimensions,
    configure_size,
    wbg_theme,
)

__all__ = [
    # Theme functions
    "enable",
    "wbg_theme",
    "configure_size",
    "calculate_dimensions",
    # Size context managers
    "small",
    "medium",
    "large",
    # Formatting utilities
    "format_number",
    "format_date",
    "d3_number_format",
    "d3_date_format",
    "vega_scale_labelExpr",
    # Caption and interaction helpers
    "add_caption",
    "add_hover",
    "point_selection",
    "interval_selection",
    # Responsive sizing constants
    "SIZE_BREAKPOINTS",
    "TYPOGRAPHY",
    "SPACING",
    "ASPECT_RATIOS",
    "DEFAULT_DIMENSIONS",
    # Color palettes
    "CATEGORICAL",
    "CATEGORICAL_TEXT",
    "REGIONS",
    "REGIONS_TEXT",
    "REGIONS_SECONDARY",
    "INCOME",
    "INCOME_LIST",
    "GENDER",
    "URBANIZATION",
    "AGE",
    "BINARY",
    "SEQ_BAD_TO_GOOD",
    "SEQ_GOOD_TO_BAD",
    "SEQ_BLUE",
    "SEQ_YELLOW",
    "SEQ_PURPLE",
    "SEQ_GREEN",
    "SEQ_RED",
    "DIV_DEFAULT",
    "DIV_NEUTRAL",
    "DIV_ALTERNATIVE",
    "SELECTION_PRIMARY",
    "SELECTION_SECONDARY",
    "REFERENCE",
    "NO_DATA",
    "TOTAL",
    "PILLARS",
    "GREY_100",
    "GREY_200",
    "GREY_300",
    "GREY_400",
    "GREY_500",
    "TEXT",
    "TEXT_SUBTLE",
]

# Register theme variants with Altair on import
alt.themes.register("wbg", wbg_theme)  # Default (medium)
alt.themes.register("wbg-small", lambda: wbg_theme(size="small"))
alt.themes.register("wbg-medium", lambda: wbg_theme(size="medium"))
alt.themes.register("wbg-large", lambda: wbg_theme(size="large"))


def enable(size: Literal["small", "medium", "large"] = "medium") -> None:
    """Enable the WBG theme globally for all Altair charts.

    Parameters
    ----------
    size
        Size category for typography and spacing: 'small' (<400px width),
        'medium' (400-700px), or 'large' (>700px). Defaults to 'medium'.

    Examples
    --------
    >>> import attaviz
    >>> attaviz.enable()  # Use medium size (default)
    >>> attaviz.enable(size='large')  # Use large typography/spacing
    """
    theme_name = "wbg" if size == "medium" else f"wbg-{size}"
    alt.themes.enable(theme_name)


# ---------------------------------------------------------------------------
# Caption support
# ---------------------------------------------------------------------------
def add_caption(
    chart,
    text: str,
    *,
    align: Literal["left", "center", "right"] = "left",
):
    """Add a styled caption below a chart.

    Creates a text element with WBG styling (regular weight, small font,
    150% line height, subtle text color) and concatenates it below the chart.

    Parameters
    ----------
    chart
        An Altair chart object.
    text
        The caption text. Include any prefix like "Source: " or "Note: "
        in the string itself. Use ``\\n`` to split across lines.
    align
        Text alignment: "left", "center", or "right". Defaults to "left",
        which matches the WBG spec (notes/sources anchor to the same
        container edge as the chart title). "center" and "right" are
        provided for flexibility but are off-spec.

    Returns
    -------
    alt.VConcatChart
        The original chart with caption below.

    Examples
    --------
    >>> chart = alt.Chart(data).mark_bar().encode(...)
    >>> chart_with_caption = attaviz.add_caption(
    ...     chart,
    ...     "Source: World Bank Development Indicators, 2023"
    ... )
    >>> chart_with_caption = attaviz.add_caption(
    ...     chart,
    ...     "Note: Data excludes 2020 due to COVID-19.",
    ...     align="right"
    ... )
    """
    # Detect width from chart
    width = getattr(chart, "width", None)
    if not isinstance(width, int):
        if hasattr(chart, "to_dict"):
            spec = chart.to_dict(format="vega") if alt.data_transformers.active == "vegafusion" else chart.to_dict()
            width = spec.get("width", DEFAULT_DIMENSIONS["medium"][0])
            if not isinstance(width, int):
                width = DEFAULT_DIMENSIONS["medium"][0]
        else:
            width = DEFAULT_DIMENSIONS["medium"][0]

    size = _get_size_category(width)
    typo = TYPOGRAPHY[size]
    space = SPACING[size]

    font_s = typo["S"]
    line_height = round(font_s * LINE_HEIGHT_LONG)

    anchor = {"left": "start", "center": "middle", "right": "end"}[align]
    title_text = text.split("\n") if "\n" in text else text

    caption = alt.TitleParams(
        text=title_text,
        orient="bottom",
        anchor=anchor,
        font=FONT,
        fontSize=font_s,
        fontWeight=400,
        color=TEXT_SUBTLE,
        lineHeight=line_height,
        offset=space["xl"],
    )

    return alt.vconcat(chart).properties(title=caption)
