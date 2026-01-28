"""World Bank Group data visualization theme for Altair.

Usage::

    import altair as alt
    import altair_theme_wbg

    altair_theme_wbg.enable()

    # Now all charts use the WBG theme
    chart = alt.Chart(...).mark_bar().encode(...)
"""

from __future__ import annotations

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
from .theme import wbg_theme

__all__ = [
    "enable",
    "wbg_theme",
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

# Register the theme with Altair on import
alt.themes.register("wbg", wbg_theme)


def enable() -> None:
    """Enable the WBG theme globally for all Altair charts."""
    alt.themes.enable("wbg")
