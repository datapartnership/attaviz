"""World Bank Group data visualization theme for Altair.

Usage::

    import altair as alt
    import altair_theme_wbg as wbg

    wbg.enable()

    # Now all charts use the WBG theme
    chart = alt.Chart(...).mark_bar().encode(...)

    # Use size-specific themes
    wbg.enable(size='large')

    # Per-chart sizing
    chart = wbg.configure_size(chart, width=400, aspect_ratio='16:9')

    # Calculate dimensions
    w, h = wbg.calculate_dimensions(800, '16:9')  # (800, 450)
"""

from __future__ import annotations

from typing import Literal

import altair as alt

from .colors import (  # noqa: F401 – re-exported as public API
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
    SIZE_BREAKPOINTS,
    SPACING,
    TYPOGRAPHY,
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
    >>> import altair_theme_wbg as wbg
    >>> wbg.enable()  # Use medium size (default)
    >>> wbg.enable(size='large')  # Use large typography/spacing
    """
    theme_name = "wbg" if size == "medium" else f"wbg-{size}"
    alt.themes.enable(theme_name)
