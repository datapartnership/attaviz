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
    align: Literal["left", "center", "right"] = "right",
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
        in the string itself.
    align
        Text alignment: "left", "center", or "right". Defaults to "left".

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
    # Detect width from chart. Altair uses an Undefined sentinel (not None)
    # for unset properties, so check for a concrete int instead.
    width = getattr(chart, "width", None)
    if not isinstance(width, int):
        if hasattr(chart, "to_dict"):
            spec = chart.to_dict()
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

    caption_chart = (
        alt.Chart({"values": [{}]})
        .mark_text(
            align=align,
            baseline="top",
            font=FONT,
            fontSize=font_s,
            fontWeight=400,
            color=TEXT_SUBTLE,
            lineHeight=line_height,
        )
        .encode(text=alt.value(text))
        .properties(width=width, height=font_s * 2)
    )

    return alt.vconcat(chart, caption_chart, spacing=space["m"])


# ---------------------------------------------------------------------------
# Selection and hover helpers
# ---------------------------------------------------------------------------
def add_hover(
    chart,
    *,
    opacity_normal: float = 0.6,
    opacity_hover: float = 1.0,
):
    """Add hover highlighting to chart marks.

    Adds a pointer-based selection that increases opacity on hover,
    creating a visual highlight effect.

    Parameters
    ----------
    chart
        An Altair chart object.
    opacity_normal
        Opacity for non-hovered marks. Defaults to 0.6.
    opacity_hover
        Opacity for hovered marks. Defaults to 1.0.

    Returns
    -------
    alt.Chart
        The chart with hover interaction added.

    Examples
    --------
    >>> chart = attaviz.add_hover(
    ...     alt.Chart(data).mark_bar().encode(...)
    ... )
    >>> # Bars will highlight on hover
    """
    hover = alt.selection_point(on="pointerover", empty=False)
    return chart.add_params(hover).encode(
        opacity=alt.condition(
            hover, alt.value(opacity_hover), alt.value(opacity_normal)
        )
    )


def point_selection(name: str = "select", **kwargs):
    """Create a point selection with WBG defaults.

    Parameters
    ----------
    name
        Name for the selection parameter. Defaults to "select".
    **kwargs
        Additional arguments passed to alt.selection_point().

    Returns
    -------
    alt.SelectionParameter
        A configured point selection.

    Examples
    --------
    >>> select = attaviz.point_selection()
    >>> chart = alt.Chart(data).mark_point().encode(...).add_params(select)
    """
    return alt.selection_point(name=name, **kwargs)


def interval_selection(name: str = "brush"):
    """Create an interval (brush) selection with WBG styling.

    The brush uses the WBG selection primary color with appropriate
    opacity and stroke styling.

    Parameters
    ----------
    name
        Name for the selection parameter. Defaults to "brush".

    Returns
    -------
    alt.SelectionParameter
        A configured interval selection with WBG styling.

    Examples
    --------
    >>> brush = attaviz.interval_selection()
    >>> chart = alt.Chart(data).mark_point().encode(...).add_params(brush)
    """
    return alt.selection_interval(
        name=name,
        mark=alt.BrushConfig(
            fill=SELECTION_PRIMARY,
            fillOpacity=0.15,
            stroke=SELECTION_PRIMARY,
        ),
    )
