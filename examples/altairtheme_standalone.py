"""Standalone World Bank Group Altair theme.

A single-file version of the ``altair_theme_wbg`` package that can be dropped
into any project without pip installing.

Usage::

    # Copy this file into your project, then:
    import altair as alt
    import altair_theme_wbg as wbg

    wbg.enable()

    # All charts now use the WBG theme
    chart = alt.Chart(...).mark_bar().encode(...)

    # Color palettes are also available:
    alt.Scale(range=wbg.CATEGORICAL)
"""

from __future__ import annotations

import altair as alt

# ===========================================================================
# Colors
# ===========================================================================
# All colors are sourced from the WBG Data Visualization Style Guide:
# https://worldbank.github.io/data-visualization-style-guide/colors

# ---------------------------------------------------------------------------
# Categorical palette
# ---------------------------------------------------------------------------
CATEGORICAL = [
    "#34A7F2",  # cat1
    "#FF9800",  # cat2
    "#664AB6",  # cat3
    "#4EC2C0",  # cat4
    "#F3578E",  # cat5
    "#081079",  # cat6
    "#0C7C68",  # cat7
    "#AA0000",  # cat8
    "#DDDA21",  # cat9
]

# Text variants
CATEGORICAL_TEXT = [
    "#106CA1",  # cat1Text
    "#B65F0C",  # cat2Text
    "#664AB6",  # cat3Text
    "#208383",  # cat4Text
    "#BB3B64",  # cat5Text
    "#081079",  # cat6Text
    "#0C7C68",  # cat7Text
    "#AA0000",  # cat8Text
    "#767712",  # cat9Text
]

# ---------------------------------------------------------------------------
# Region colors
# ---------------------------------------------------------------------------
REGIONS = {
    "NAC": "#34A7F2",
    "SSF": "#FF9800",
    "MEA": "#664AB6",
    "SAS": "#4EC2C0",
    "EAS": "#F3578E",
    "LCN": "#0C7C68",
    "ECS": "#AA0000",
    "AFW": "#DDDA21",
    "AFE": "#FF9800",
    "WLD": "#081079",
}

REGIONS_TEXT = {
    "NAC": "#106CA1",
    "SSF": "#B65F0C",
    "MEA": "#664AB6",
    "SAS": "#208383",
    "EAS": "#BB3B64",
    "LCN": "#0C7C68",
    "ECS": "#AA0000",
    "AFW": "#767712",
    "AFE": "#B65F0C",
    "WLD": "#081079",
}

# Secondary region series
REGIONS_SECONDARY = {
    "NAC": ["#34A7F2", "#80D2E8", "#163C6C", "#106CA1"],
    "SSF": ["#FF9800", "#FFD554", "#8F3B18", "#C2660D"],
    "MEA": ["#664AB6", "#B38FD8", "#462F98", "#EDC2F1"],
    "SAS": ["#4EC2C0", "#228B8B", "#006061", "#95E2E2"],
    "EAS": ["#F3578E", "#F8A8DF", "#BB3B64", "#801E37"],
    "LCN": ["#0C7C68", "#54AE89", "#084D31", "#9ADEAA"],
    "ECS": ["#AA0000", "#EB6E51", "#FF9E75", "#D43729"],
    "AFW": ["#DDDA21", "#7B7C13", "#ABAA22", "#4E5200"],
    "AFE": ["#FF9800", "#FFD554", "#8F3B18", "#C2660D"],
}

# ---------------------------------------------------------------------------
# Income groups
# ---------------------------------------------------------------------------
INCOME = {
    "HIC": "#016B6C",
    "UMC": "#73AF48",
    "LMC": "#DB95D7",
    "LIC": "#3B4DA6",
}

INCOME_LIST = ["#016B6C", "#73AF48", "#DB95D7", "#3B4DA6"]

# ---------------------------------------------------------------------------
# Gender
# ---------------------------------------------------------------------------
GENDER = {
    "female": "#FF9800",
    "male": "#664AB6",
    "diverse": "#4EC2C0",
}

# ---------------------------------------------------------------------------
# Urbanization
# ---------------------------------------------------------------------------
URBANIZATION = {
    "urban": "#6D88D1",
    "rural": "#54AE89",
}

# ---------------------------------------------------------------------------
# Age groups
# ---------------------------------------------------------------------------
AGE = [
    "#F8A8DF",  # youngest
    "#B38FD8",  # younger
    "#462F98",  # middle
    "#6D88D1",  # older
    "#A1C6FF",  # oldest
]

# ---------------------------------------------------------------------------
# Binary
# ---------------------------------------------------------------------------
BINARY = {
    "yes": "#0071BC",
    "no": "#EBEEF4",
}

# ---------------------------------------------------------------------------
# Sequential palettes
# ---------------------------------------------------------------------------
SEQ_BAD_TO_GOOD = ["#FDF6DB", "#A1CBCF", "#5D99C2", "#2868A0", "#023B6F"]
SEQ_GOOD_TO_BAD = ["#E3F6FD", "#91C5F0", "#8B8AC0", "#88506E", "#691B15"]

SEQ_BLUE = ["#E3F6FD", "#75CCEC", "#089BD4", "#0169A1", "#023B6F"]
SEQ_YELLOW = ["#FDF7DB", "#ECB63A", "#BE792B", "#8D4117", "#5C0000"]
SEQ_PURPLE = ["#FFE2FF", "#D3ACE6", "#A37ACD", "#6F4CB4", "#2F1E9C"]
SEQ_GREEN = ["#D2FFE1", "#8AD4A7", "#54A67F", "#27795A", "#084D31"]
SEQ_RED = ["#FFD6B9", "#F99C78", "#E56245", "#C1261A", "#870000"]

# ---------------------------------------------------------------------------
# Diverging palettes
# ---------------------------------------------------------------------------
DIV_DEFAULT = [
    "#920000",  # neg3
    "#BD6126",  # neg2
    "#E3A763",  # neg1
    "#EFEFEF",  # mid
    "#80BDE7",  # pos1
    "#3587C3",  # pos2
    "#025288",  # pos3
]

DIV_NEUTRAL = [
    "#24768E",  # L3
    "#4EA2AC",  # L2
    "#98CBCC",  # L1
    "#EFEFEF",  # mid
    "#D1AEE3",  # R1
    "#A873C4",  # R2
    "#754493",  # R3
]

DIV_ALTERNATIVE = [
    "#002C8B",  # L3
    "#4868AF",  # L2
    "#79A7D5",  # L1
    "#EFEFEF",  # mid
    "#ECA08C",  # R1
    "#C9573E",  # R2
    "#920000",  # R3
]

# ---------------------------------------------------------------------------
# Functional colors
# ---------------------------------------------------------------------------
SELECTION_PRIMARY = "#0071BC"
SELECTION_SECONDARY = "#8963C1"
REFERENCE = "#8A969F"
NO_DATA = "#CED4DE"
TOTAL = "#163C6C"

# ---------------------------------------------------------------------------
# Pillar colors
# ---------------------------------------------------------------------------
PILLARS = {
    "people": "#F7B841",
    "planet": "#07AB50",
    "prosperity": "#872C8F",
    "infrastructure": "#91302F",
    "digital": "#5D6472",
    "corporate": "#004972",
}

# ---------------------------------------------------------------------------
# Grey scale
# ---------------------------------------------------------------------------
GREY_500 = "#111111"
GREY_400 = "#666666"
GREY_300 = "#8A969F"
GREY_200 = "#CED4DE"
GREY_100 = "#EBEEF4"

# Text colors
TEXT = "#111111"
TEXT_SUBTLE = "#666666"


# ===========================================================================
# Theme
# ===========================================================================

from typing import Literal

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
                "stroke": GREY_300,
                "strokeWidth": 0.5,
            },
            "geoshape": {
                "stroke": GREY_400,
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
                "color": TEXT,
                "anchor": "start",
                "offset": space["xl"],
                "subtitleFont": FONT,
                "subtitleFontSize": font_m,
                "subtitleFontWeight": FONT_WEIGHT_REGULAR,
                "subtitleLineHeight": round(font_m * LINE_HEIGHT_SHORT),
                "subtitleColor": TEXT_SUBTLE,
                "subtitlePadding": space["xxs"],
            },
            # -- Axes -------------------------------------------------------
            "axis": {
                "domain": False,
                "grid": True,
                "gridColor": GREY_200,
                "gridDash": [4, 2],
                "gridWidth": 1,
                "labelFont": FONT,
                "labelFontSize": font_s,
                "labelFontWeight": FONT_WEIGHT_REGULAR,
                "labelColor": TEXT_SUBTLE,
                "labelPadding": space["xxs"],
                "tickColor": GREY_200,
                "tickSize": 5,
                "tickCount": 5,
                "titleFont": FONT,
                "titleFontSize": font_s,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": TEXT,
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
                "gridColor": GREY_200,
                "gridDash": [4, 2],
                "gridWidth": 1,
            },
            "axisQuantitative": {
                "tickCount": 5,
            },
            "axisTemporal": {
                "grid": False,
            },
            # -- Legend ------------------------------------------------------
            "legend": {
                "labelFont": FONT,
                "labelFontSize": font_s,
                "labelFontWeight": FONT_WEIGHT_SEMIBOLD,
                "labelColor": TEXT,
                "titleFont": FONT,
                "titleFontSize": font_s,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": TEXT,
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
                "category": CATEGORICAL,
                "diverging": DIV_DEFAULT,
                "heatmap": SEQ_BLUE,
                "ordinal": SEQ_BLUE,
                "ramp": SEQ_BLUE,
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
                "labelColor": TEXT,
                "titleFont": FONT,
                "titleFontSize": font_m,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": TEXT,
            },
            # -- Concat / Facet spacing -------------------------------------
            "concat": {"spacing": space["l"]},
            "facet": {"spacing": space["l"]},
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


# ===========================================================================
# Theme registration
# ===========================================================================

alt.themes.register("wbg", wbg_theme)  # Default (medium)
alt.themes.register("wbg-small", lambda: wbg_theme(size="small"))
alt.themes.register("wbg-medium", lambda: wbg_theme(size="medium"))
alt.themes.register("wbg-large", lambda: wbg_theme(size="large"))


def enable(size: SizeCategory = "medium") -> None:
    """Enable the WBG theme globally for all Altair charts.

    Parameters
    ----------
    size
        Size category for typography and spacing: 'small' (<400px width),
        'medium' (400-700px), or 'large' (>700px). Defaults to 'medium'.

    Examples
    --------
    >>> import altair_theme_wbg as wbg
    >>> wbg.enable()  # Use medium size (default)
    >>> wbg.enable(size='large')  # Use large typography/spacing
    """
    theme_name = "wbg" if size == "medium" else f"wbg-{size}"
    alt.themes.enable(theme_name)
