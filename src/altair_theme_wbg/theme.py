"""World Bank Group Altair theme.

Implements the WBG Data Visualization Style Guide as an Altair theme.
Reference: https://wbg-vis-design.vercel.app/
"""

from __future__ import annotations

from . import colors

# ---------------------------------------------------------------------------
# Typography constants (medium chart width: 400–700 px)
# ---------------------------------------------------------------------------
FONT = "Open Sans, sans-serif"

FONT_SIZE_S = 13
FONT_SIZE_M = 15
FONT_SIZE_L = 18

FONT_WEIGHT_REGULAR = 400
FONT_WEIGHT_SEMIBOLD = 600
FONT_WEIGHT_BOLD = 700

LINE_HEIGHT_SHORT = 1.2   # titles, labels
LINE_HEIGHT_LONG = 1.5    # notes, paragraphs


def wbg_theme() -> dict:
    """Return the WBG Vega-Lite theme configuration."""
    return {
        "config": {
            # -- Background -------------------------------------------------
            "background": "white",
            "padding": 20,

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
                "fontSize": FONT_SIZE_L,
                "fontWeight": FONT_WEIGHT_BOLD,
                "lineHeight": round(FONT_SIZE_L * LINE_HEIGHT_SHORT),
                "color": colors.TEXT,
                "anchor": "start",
                "offset": 12,
                "subtitleFont": FONT,
                "subtitleFontSize": FONT_SIZE_M,
                "subtitleFontWeight": FONT_WEIGHT_REGULAR,
                "subtitleLineHeight": round(FONT_SIZE_M * LINE_HEIGHT_SHORT),
                "subtitleColor": colors.TEXT_SUBTLE,
                "subtitlePadding": 6,
            },

            # -- Axes -------------------------------------------------------
            "axis": {
                "domain": False,
                "grid": True,
                "gridColor": colors.GREY_200,
                "gridDash": [4, 2],
                "gridWidth": 1,
                "labelFont": FONT,
                "labelFontSize": FONT_SIZE_S,
                "labelFontWeight": FONT_WEIGHT_REGULAR,
                "labelColor": colors.TEXT_SUBTLE,
                "labelPadding": 8,
                "tickColor": colors.GREY_200,
                "tickSize": 5,
                "tickCount": 5,
                "titleFont": FONT,
                "titleFontSize": FONT_SIZE_S,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
                "titlePadding": 10,
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
            "axisTemporal": {
                "grid": False,
            },

            # -- Legend ------------------------------------------------------
            "legend": {
                "labelFont": FONT,
                "labelFontSize": FONT_SIZE_S,
                "labelFontWeight": FONT_WEIGHT_SEMIBOLD,
                "labelColor": colors.TEXT,
                "titleFont": FONT,
                "titleFontSize": FONT_SIZE_S,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
                "titlePadding": 8,
                "symbolSize": 196,  # 14x14 px dot
                "symbolStrokeWidth": 0,
                "padding": 16,
                "offset": 4,
                "orient": "right",
                "labelLimit": 200,
                "titleLimit": 200,
            },

            # -- View -------------------------------------------------------
            "view": {
                "stroke": None,
                "continuousWidth": 600,
                "continuousHeight": 400,
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
                "labelFontSize": FONT_SIZE_S,
                "labelFontWeight": FONT_WEIGHT_SEMIBOLD,
                "labelColor": colors.TEXT,
                "titleFont": FONT,
                "titleFontSize": FONT_SIZE_M,
                "titleFontWeight": FONT_WEIGHT_SEMIBOLD,
                "titleColor": colors.TEXT,
            },

            # -- Concat / Facet spacing -------------------------------------
            "concat": {"spacing": 20},
            "facet": {"spacing": 20},
        }
    }
