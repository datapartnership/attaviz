"""World Bank Group Altair theme.

Implements the WBG Data Visualization Style Guide as an Altair theme.
Reference: https://worldbank.github.io/data-visualization-style-guide/
"""

from __future__ import annotations

from typing import Literal

from . import colors

# ---------------------------------------------------------------------------
# Typography constants
# ---------------------------------------------------------------------------
FONT = "Open Sans, sans-serif"

FONT_WEIGHT_REGULAR = 400
FONT_WEIGHT_SEMIBOLD = 600
FONT_WEIGHT_BOLD = 700

LINE_HEIGHT_SHORT = 1.2  # titles, labels
LINE_HEIGHT_LONG = 1.5  # notes, paragraphs

# ---------------------------------------------------------------------------
# Responsive sizing constants
# ---------------------------------------------------------------------------
SizeCategory = Literal["small", "medium", "large"]

SIZE_BREAKPOINTS = {"small": 400, "medium": 700}

# Typography scales by size category (S/M/L font sizes)
TYPOGRAPHY: dict[str, dict[str, int]] = {
    "small": {"S": 12, "M": 14, "L": 16},
    "medium": {"S": 13, "M": 15, "L": 18},
    "large": {"S": 14, "M": 16, "L": 20},
}

# Spacing scales by size category
SPACING: dict[str, dict[str, int]] = {
    "small": {"xxs": 2, "xs": 4, "s": 6, "m": 12, "l": 14, "xl": 16},
    "medium": {"xxs": 3, "xs": 6, "s": 9, "m": 15, "l": 18, "xl": 21},
    "large": {"xxs": 4, "xs": 8, "s": 12, "m": 16, "l": 20, "xl": 24},
}

# Named aspect ratios
ASPECT_RATIOS: dict[str, float] = {
    "16:9": 16 / 9,
    "4:3": 4 / 3,
    "3:2": 3 / 2,
    "1:1": 1.0,
    "2:1": 2.0,
    "square": 1.0,
    "widescreen": 16 / 9,
}

# Default dimensions for each size category (using 3:2 aspect ratio)
DEFAULT_DIMENSIONS: dict[str, tuple[int, int]] = {
    "small": (350, 233),
    "medium": (600, 400),
    "large": (800, 533),
}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _get_size_category(width: int) -> SizeCategory:
    """Return 'small', 'medium', or 'large' based on chart width."""
    if width < SIZE_BREAKPOINTS["small"]:
        return "small"
    elif width < SIZE_BREAKPOINTS["medium"]:
        return "medium"
    else:
        return "large"


def calculate_dimensions(
    width: int,
    aspect_ratio: str | float = "3:2",
) -> tuple[int, int]:
    """Calculate (width, height) from width and aspect ratio.

    Parameters
    ----------
    width
        The desired chart width in pixels.
    aspect_ratio
        Either a named ratio ('16:9', '4:3', '3:2', '1:1', '2:1', 'square',
        'widescreen') or a numeric ratio (width/height).

    Returns
    -------
    tuple[int, int]
        The (width, height) tuple.

    Examples
    --------
    >>> calculate_dimensions(800, '16:9')
    (800, 450)
    >>> calculate_dimensions(600, '3:2')
    (600, 400)
    >>> calculate_dimensions(400, 1.5)
    (400, 267)
    """
    if isinstance(aspect_ratio, str):
        ratio = ASPECT_RATIOS.get(aspect_ratio)
        if ratio is None:
            raise ValueError(
                f"Unknown aspect ratio '{aspect_ratio}'. "
                f"Valid options: {list(ASPECT_RATIOS.keys())}"
            )
    else:
        ratio = float(aspect_ratio)

    height = round(width / ratio)
    return (width, height)


def wbg_theme(
    size: SizeCategory = "medium",
    *,
    width: int | None = None,
    height: int | None = None,
    aspect_ratio: str | float | None = None,
) -> dict:
    """Return the WBG Vega-Lite theme configuration.

    Parameters
    ----------
    size
        Size category for typography and spacing: 'small', 'medium', or 'large'.
        Ignored if ``width`` is provided (auto-detected from width).
    width
        Explicit chart width in pixels. If provided, the size category is
        auto-detected based on breakpoints (<400px = small, 400-700px = medium,
        >700px = large).
    height
        Explicit chart height in pixels. If not provided and ``width`` is set,
        calculated from ``aspect_ratio``.
    aspect_ratio
        Aspect ratio for calculating height from width. Can be a named ratio
        ('16:9', '4:3', '3:2', '1:1', '2:1', 'square', 'widescreen') or a
        numeric ratio (width/height). Defaults to '3:2'.

    Returns
    -------
    dict
        A Vega-Lite theme configuration dictionary.

    Examples
    --------
    >>> wbg_theme()  # Default medium size, 600x400
    >>> wbg_theme(size='large')  # Large typography, 800x533
    >>> wbg_theme(width=900, aspect_ratio='16:9')  # Custom dimensions
    """
    # Determine size category and dimensions
    if width is not None:
        size = _get_size_category(width)
        if height is None:
            _, height = calculate_dimensions(width, aspect_ratio or "3:2")
        chart_width, chart_height = width, height
    else:
        chart_width, chart_height = DEFAULT_DIMENSIONS[size]
        if height is not None:
            chart_height = height

    typo = TYPOGRAPHY[size]
    space = SPACING[size]

    font_s = typo["S"]
    font_m = typo["M"]
    font_l = typo["L"]

    return {
        "config": {
            # -- Background -------------------------------------------------
            "background": "white",
            "padding": space["m"],
            # -- Default mark properties ------------------------------------
            "mark": {
                "tooltip": True,
            },
            "point": {
                "filled": True,
                "size": 60,
                "stroke": "white",
                "strokeWidth": 1,
            },
            "circle": {
                "filled": True,
                "stroke": "white",
                "strokeWidth": 1,
            },
            "square": {
                "filled": True,
                "stroke": "white",
                "strokeWidth": 1,
            },
            "line": {
                "strokeWidth": 4,
                "strokeCap": "round",
                "strokeJoin": "round",
            },
            "bar": {
                "cornerRadiusEnd": 0,
            },
            "area": {
                "opacity": 0.7,
            },
            "arc": {
                "stroke": "white",
                "strokeWidth": 1,
            },
            "rect": {
                "stroke": colors.GREY_300,
                "strokeWidth": 0.5,
            },
            "geoshape": {
                "stroke": colors.GREY_400,
                "strokeWidth": 0.3,
                "strokeJoin": "round",
                "strokeCap": "round",
            },
            # -- Title & subtitle -------------------------------------------
            "title": {
                "font": FONT,
                "fontSize": font_l,
                "fontWeight": FONT_WEIGHT_BOLD,
                "lineHeight": round(font_l * LINE_HEIGHT_SHORT),
                "color": colors.TEXT,
                "anchor": "start",
                "offset": space["xl"],
                "subtitleFont": FONT,
                "subtitleFontSize": font_m,
                "subtitleFontWeight": FONT_WEIGHT_REGULAR,
                "subtitleLineHeight": round(font_m * LINE_HEIGHT_SHORT),
                "subtitleColor": colors.TEXT_SUBTLE,
                "subtitlePadding": space["xxs"],
            },
            # -- Axes -------------------------------------------------------
            "axis": {
                "domain": False,
                "grid": True,
                "gridColor": colors.GREY_200,
                "gridDash": [4, 2],
                "gridWidth": 1,
                "labelFont": FONT,
                "labelFontSize": font_s,
                "labelFontWeight": FONT_WEIGHT_REGULAR,
                "labelColor": colors.TEXT_SUBTLE,
                "labelPadding": space["xxs"],
                "tickColor": colors.GREY_200,
                "tickSize": 5,
                "tickCount": 5,
                "titleFont": FONT,
                "titleFontSize": font_s,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
                "titlePadding": space["s"],
            },
            "axisX": {
                "grid": False,
                "tickSize": 0,
                "labelAngle": 0,
            },
            "axisY": {
                "domain": False,
                "ticks": False,
                "gridColor": colors.GREY_200,
                "gridDash": [4, 2],
                "gridWidth": 1,
            },
            "axisQuantitative": {
                "tickCount": 5,
            },
            "axisBand": {
                "labelPadding": space["xs"],
                "tickSize": 0,
            },
            "axisTemporal": {
                "grid": False,
            },
            # -- Legend ------------------------------------------------------
            "legend": {
                "labelFont": FONT,
                "labelFontSize": font_s,
                "labelFontWeight": FONT_WEIGHT_SEMIBOLD,
                "labelColor": colors.TEXT,
                "titleFont": FONT,
                "titleFontSize": font_s,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
                "titlePadding": space["xxs"],
                "symbolSize": 196,  # 14x14 px dot
                "symbolStrokeWidth": 0,
                "padding": space["m"],
                "offset": space["xl"],
                "columnPadding": space["xl"],
                "orient": "bottom",
                "labelLimit": 200,
                "titleLimit": 200,
            },
            # -- View -------------------------------------------------------
            "view": {
                "stroke": None,
                "continuousWidth": chart_width,
                "continuousHeight": chart_height,
            },
            # -- Color ranges -----------------------------------------------
            "range": {
                "category": colors.CATEGORICAL,
                "diverging": colors.DIV_DEFAULT,
                "heatmap": colors.SEQ_BLUE,
                "ordinal": colors.SEQ_BLUE,
                "ramp": colors.SEQ_BLUE,
            },
            # -- Scale defaults ----------------------------------------------
            "scale": {
                "bandPaddingInner": 0.2,
                "bandPaddingOuter": 0.1,
                "pointPadding": 0.5,
            },
            # -- Header (facets) --------------------------------------------
            "header": {
                "labelFont": FONT,
                "labelFontSize": font_s,
                "labelFontWeight": FONT_WEIGHT_SEMIBOLD,
                "labelColor": colors.TEXT,
                "titleFont": FONT,
                "titleFontSize": font_m,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
            },
            # -- Concat / Facet spacing -------------------------------------
            "concat": {"spacing": space["l"]},
            "facet": {"spacing": space["l"]},
            # -- Selection styling ------------------------------------------
            "selection": {
                "point": {
                    "on": "click",
                    "clear": "dblclick",
                },
                "interval": {
                    "mark": {
                        "fill": colors.SELECTION_PRIMARY,
                        "fillOpacity": 0.15,
                        "stroke": colors.SELECTION_PRIMARY,
                        "strokeWidth": 1,
                    },
                },
            },
        }
    }


def configure_size(
    chart,
    width: int,
    height: int | None = None,
    aspect_ratio: str | float = "3:2",
):
    """Apply size-appropriate configuration to a single chart.

    This function applies responsive typography and spacing to an individual
    chart without changing the global theme. Useful for per-chart sizing.

    Parameters
    ----------
    chart
        An Altair chart object.
    width
        The desired chart width in pixels.
    height
        The desired chart height in pixels. If not provided, calculated from
        ``aspect_ratio``.
    aspect_ratio
        Aspect ratio for calculating height from width. Can be a named ratio
        ('16:9', '4:3', '3:2', '1:1', '2:1', 'square', 'widescreen') or a
        numeric ratio (width/height). Defaults to '3:2'.

    Returns
    -------
    alt.Chart
        The chart with size-appropriate configuration applied.

    Examples
    --------
    >>> chart = alt.Chart(data).mark_bar().encode(...)
    >>> chart = configure_size(chart, width=400, aspect_ratio='16:9')
    """
    if height is None:
        _, height = calculate_dimensions(width, aspect_ratio)

    size = _get_size_category(width)
    typo = TYPOGRAPHY[size]
    space = SPACING[size]

    font_s = typo["S"]
    font_m = typo["M"]
    font_l = typo["L"]

    return (
        chart.properties(width=width, height=height)
        .configure_title(
            fontSize=font_l,
            lineHeight=round(font_l * LINE_HEIGHT_SHORT),
            offset=space["l"],
            subtitleFontSize=font_m,
            subtitleLineHeight=round(font_m * LINE_HEIGHT_SHORT),
            subtitlePadding=space["xxs"],
        )
        .configure_axis(
            labelFontSize=font_s,
            labelPadding=space["xxs"],
            titleFontSize=font_s,
            titlePadding=space["s"],
        )
        .configure_legend(
            labelFontSize=font_s,
            titleFontSize=font_s,
            titlePadding=space["s"],
            padding=space["m"],
            offset=space["xl"],
            orient="bottom",
        )
        .configure_header(
            labelFontSize=font_s,
            titleFontSize=font_m,
        )
    )
