"""Publication tables using Great Tables and Attaviz theme values."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from . import colors
from .theme import (
    FONT,
    FONT_WEIGHT_BOLD,
    FONT_WEIGHT_REGULAR,
    FONT_WEIGHT_SEMIBOLD,
    LINE_HEIGHT_LONG,
    SPACING,
    TYPOGRAPHY,
)

if TYPE_CHECKING:
    from great_tables import GT


def table(
    data: pd.DataFrame,
    *,
    title: str | None = None,
    subtitle: str | None = None,
    source: str | None = None,
) -> GT:
    """Create a styled Great Tables table from a pandas DataFrame.

    Install ``attaviz[tables]`` first. Returns a native ``GT`` object so
    formatting, labels, footnotes, and exports can use Great Tables directly.
    Numbers retain their precision unless explicitly formatted by the caller;
    missing values display as ``N/A``. The DataFrame index is not displayed.
    Input data is copied. Title, subtitle, and source are plain text. Tables
    size to their content; use native ``cols_width()`` and ``tab_options()``
    to override widths or ``opt_row_striping()`` for subtle row shading.

    Typography and colors follow Attaviz's medium theme. Horizontal rules
    are an Attaviz default, rather than a table-specific WBG specification.

    Examples
    --------
    >>> result = table(data, title="Population", source="Source: World Bank")
    >>> result = result.fmt_integer(columns="population")
    """
    try:
        from great_tables import GT, loc, style
    except ImportError as exc:
        raise ImportError(
            "table() requires the 'tables' extra: pip install \"attaviz[tables]\""
        ) from exc

    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")
    if data.empty:
        raise ValueError("data must contain at least one row and column")
    if not data.columns.is_unique or not all(
        isinstance(column, str) for column in data.columns
    ):
        raise ValueError("data must have unique string column names")
    if subtitle is not None and title is None:
        raise ValueError("subtitle requires a title")

    typo = TYPOGRAPHY["medium"]
    space = SPACING["medium"]
    result = (
        GT(data.copy())
        .sub_missing(missing_text="N/A")
        .tab_options(
            table_font_names=[font.strip() for font in FONT.split(",")],
            table_font_size=typo["S"],
            table_font_weight=FONT_WEIGHT_REGULAR,
            table_font_color=colors.TEXT,
            table_background_color="white",
            table_width="auto",
            table_margin_left="0px",
            table_margin_right="0px",
            table_border_top_style="none",
            table_border_bottom_style="none",
            heading_align="left",
            heading_title_font_size=typo["L"],
            heading_subtitle_font_size=typo["M"],
            heading_subtitle_font_weight=FONT_WEIGHT_REGULAR,
            heading_padding=space["s"],
            heading_padding_horizontal=0,
            heading_border_bottom_style="none",
            column_labels_font_weight=FONT_WEIGHT_SEMIBOLD,
            column_labels_padding=space["xs"],
            column_labels_padding_horizontal=space["s"],
            column_labels_border_top_style="none",
            column_labels_border_bottom_width="1px",
            column_labels_border_bottom_color=colors.GREY_300,
            table_body_hlines_color=colors.GREY_200,
            table_body_border_top_style="none",
            table_body_border_bottom_width="1px",
            table_body_border_bottom_color=colors.GREY_200,
            data_row_padding=space["xs"],
            data_row_padding_horizontal=space["s"],
            row_striping_background_color=colors.GREY_100,
            quarto_disable_processing=True,
            source_notes_font_size=typo["S"],
            source_notes_padding=space["s"],
            source_notes_padding_horizontal=0,
        )
        .tab_style(style.text(weight=FONT_WEIGHT_BOLD), locations=loc.title())
        .tab_style(
            style.text(color=colors.TEXT_SUBTLE),
            locations=[loc.subtitle(), loc.source_notes()],
        )
        .tab_style(
            style.css("font-variant-numeric: tabular-nums; vertical-align: top;"),
            locations=loc.body(),
        )
        .tab_style(
            style.css(
                f"line-height: {LINE_HEIGHT_LONG}; white-space: normal; overflow: visible;"
            ),
            locations=[loc.body(), loc.column_labels()],
        )
    )
    if title is not None:
        result = result.tab_header(title=title, subtitle=subtitle)
    if subtitle is not None:
        result = result.tab_style(
            style.css("padding-bottom: 0;"), locations=loc.title()
        ).tab_style(
            style.css(f"padding-top: {space['xxs']}px;"), locations=loc.subtitle()
        )
    if source is not None:
        result = result.tab_source_note(source)
    return result
