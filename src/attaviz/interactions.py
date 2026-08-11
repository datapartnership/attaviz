"""Interactive hover helpers for Altair charts, following the WBG style guide."""

from __future__ import annotations

import altair as alt
import pandas as pd

from . import colors
from .formatting import d3_date_format


def _channel_dict(channel) -> dict:
    """Resolve an Altair encoding channel (shorthand or object form) to a plain dict."""
    return channel.to_dict()


def _x_tooltip_format(x_type: str | None, x_format: str | None) -> str | None:
    if x_format is not None:
        return x_format
    if x_type == "temporal":
        return d3_date_format("month_year")
    return None


def add_hover(
    chart: alt.Chart | alt.LayerChart,
    x: str,
    *,
    format: str = ",.2f",
    x_format: str | None = None,
    rule_color: str = colors.GREY_400,
) -> alt.LayerChart:
    """Add a nearest-point hover rule with a tooltip to a line chart.

    Detects the shape of ``chart`` and builds a matching hover rule:

    - A single ``alt.Chart`` with a ``color`` encoding (long-form data,
      one row per x/series) is pivoted so the tooltip can show every
      series' value for the nearest x.
    - An ``alt.LayerChart`` of multiple lines, each with its own ``y``
      encoding (wide-form data), is read directly with no pivot.

    Parameters
    ----------
    chart
        An already-built chart (see shapes above).
    x
        The x-field name to key the nearest-point selection on, e.g.
        ``"date"``.
    format
        D3 number format string applied to every series' tooltip value.
    x_format
        D3 format string for the x-field's tooltip entry. Defaults to a
        month-year date format for temporal x fields, or no formatting
        otherwise.
    rule_color
        Color of the hover rule mark. Defaults to ``colors.GREY_400``.

    Returns
    -------
    alt.LayerChart
        ``chart`` layered with a hover rule. Apply ``add_caption`` after
        this, not before — ``add_caption`` wraps its input in
        ``alt.vconcat``.

    Examples
    --------
    >>> lines = base.mark_line().encode(
    ...     y=alt.Y("value:Q"), color=alt.Color("variable:N", title=None)
    ... )
    >>> chart = attaviz.add_hover(lines, x="date", format=".2f")

    Known limitations
    ------------------
    - A ``transform_filter``/``transform_calculate`` applied to only *some*
      sub-layers of a wide-form ``LayerChart`` (not the first layer, or not
      uniformly across all layers) is not carried onto the hover rule and
      may cause the rule to under- or over-filter tooltip rows relative to
      what's drawn. Apply the same transform to every layer, or filter the
      source data before charting, to avoid this.
    - A bare ``alt.Chart`` whose only ``color`` encoding is a constant
      value (``color=alt.value(...)``) raises an unclear ``KeyError``
      rather than a descriptive error, since it has no ``color`` field to
      pivot on and doesn't match either supported shape.
    """
    nearest = alt.selection_point(
        nearest=True, on="pointerover", fields=[x], empty=False
    )

    if isinstance(chart, alt.LayerChart):
        for sub_layer in chart.layer:
            sub_encoding = sub_layer.encoding
            sub_color = (
                alt.Undefined if sub_encoding is alt.Undefined else sub_encoding.color
            )
            has_color_field = (
                sub_color is not alt.Undefined and "field" in _channel_dict(sub_color)
            )
            if has_color_field:
                raise ValueError(
                    "add_hover received a LayerChart with a sub-layer that has "
                    "its own `color` encoding. This shape (a layered chart "
                    "wrapping color-encoded long-form data) is not supported. "
                    "Build a single color-encoded `alt.Chart` for long-form/"
                    "melted data instead of layering it, or restructure "
                    "wide-form data as separate `y`-encoded layers with no "
                    "`color` encoding."
                )

        x_field = _channel_dict(chart.layer[0].encoding.x)["field"]
        if x_field != x:
            raise ValueError(
                f"add_hover received x={x!r}, but the chart's x-encoding "
                f"field is {x_field!r}. Pass the field that matches the "
                "chart's x-encoding."
            )
        return _add_hover_layered(chart, x, nearest, format, x_format, rule_color)

    encoding = chart.encoding
    color = alt.Undefined if encoding is alt.Undefined else encoding.color
    if color is not alt.Undefined:
        x_field = _channel_dict(chart.encoding.x)["field"]
        if x_field != x:
            raise ValueError(
                f"add_hover received x={x!r}, but the chart's x-encoding "
                f"field is {x_field!r}. Pass the field that matches the "
                "chart's x-encoding."
            )
        return _add_hover_pivot(chart, x, nearest, format, x_format, rule_color)

    raise ValueError(
        "add_hover expects a Chart with a `color` encoding (long-form data) "
        "or a LayerChart with a `y` encoding on every layer (wide-form "
        f"data). Got a {type(chart).__name__} with no color encoding and "
        "no sub-layers."
    )


def _add_hover_pivot(chart, x, nearest, format, x_format, rule_color):
    data = chart.data
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "add_hover requires in-memory data for the pivot (color-encoded) "
            f"path; got chart.data of type {type(data).__name__}. Pass a "
            "DataFrame via alt.Chart(df), not a URL or named dataset."
        )

    color_field = _channel_dict(chart.encoding.color)["field"]
    y_field = _channel_dict(chart.encoding.y)["field"]
    x_type = _channel_dict(chart.encoding.x).get("type")

    series = sorted(data[color_field].dropna().unique().tolist())

    tooltip = [
        alt.Tooltip(field=x, type=x_type, format=_x_tooltip_format(x_type, x_format))
    ]
    tooltip += [
        alt.Tooltip(field=name, type="quantitative", format=format) for name in series
    ]

    rule = (
        alt.Chart(data)
        .encode(x=chart.encoding.x)
        .transform_pivot(color_field, value=y_field, groupby=[x])
        .mark_rule(color=rule_color)
        .encode(
            opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
            tooltip=tooltip,
        )
        .add_params(nearest)
    )
    if chart.transform is not alt.Undefined:
        rule.transform = list(chart.transform) + list(rule.transform)

    lines_no_tooltip = chart.encode(tooltip=alt.value(None))
    return alt.layer(lines_no_tooltip, rule)


def _resolve_layered_transform(chart):
    """Determine the transform (if any) safe to carry onto the shared rule.

    A top-level ``chart.transform`` applies uniformly to every layer, so it
    is always safe to carry through unmodified -- but it does not excuse
    differing per-layer transforms underneath it, since a rule built from
    the top-level transform would still misrepresent layers that have their
    own, different `transform_filter`. Per-layer transforms can only be
    carried through when every layer that has one has the *same* one (or
    there is only a single layer) -- a `filter` transform drops whole rows,
    so applying just one layer's filter to a rule whose tooltip draws on
    all layers would silently hide valid data for the layers that were not
    filtered.
    """
    if len(chart.layer) > 1:
        layer_transforms = [
            layer.transform if layer.transform is not alt.Undefined else None
            for layer in chart.layer
        ]
        if not all(t is None for t in layer_transforms) and any(
            t != layer_transforms[0] for t in layer_transforms
        ):
            raise ValueError(
                "add_hover cannot build a single accurate hover rule when "
                "different layers have different transforms: the rule's "
                "tooltip draws fields from every layer, but a `filter` "
                "transform on the rule would drop rows that are valid for "
                "layers with a different (or no) filter. Apply the same "
                "transform to every layer before calling add_hover, or "
                "pre-filter the source data instead of using "
                "transform_filter per layer."
            )

    if chart.transform is not alt.Undefined:
        return list(chart.transform)

    if len(chart.layer) == 1:
        layer_transform = chart.layer[0].transform
        return list(layer_transform) if layer_transform is not alt.Undefined else None

    layer_transforms = [
        layer.transform if layer.transform is not alt.Undefined else None
        for layer in chart.layer
    ]
    if all(t is None for t in layer_transforms):
        return None
    return list(layer_transforms[0])


def _add_hover_layered(chart, x, nearest, format, x_format, rule_color):
    series = []
    for layer in chart.layer:
        encoding = layer.encoding
        y = alt.Undefined if encoding is alt.Undefined else encoding.y
        if y is alt.Undefined:
            raise ValueError(
                "add_hover expects every layer to have a `y` encoding; "
                f"found a layer with mark {layer.mark!r} and no y encoding."
            )
        y_dict = _channel_dict(y)
        field = y_dict["field"]
        title = y_dict.get("title") or field
        series.append((field, title))

    data = chart.data
    if not isinstance(data, pd.DataFrame):
        raise ValueError(
            "add_hover expects a LayerChart whose sub-layers share the same "
            "data (Altair hoists shared data to the top-level `data` "
            "attribute automatically). Got sub-layers with different data "
            "sources, or non-DataFrame data."
        )

    x_type = _channel_dict(chart.layer[0].encoding.x).get("type")

    tooltip = [
        alt.Tooltip(field=x, type=x_type, format=_x_tooltip_format(x_type, x_format))
    ]
    tooltip += [
        alt.Tooltip(field=field, type="quantitative", format=format, title=title)
        for field, title in series
    ]

    rule = (
        alt.Chart(data)
        .encode(x=chart.layer[0].encoding.x)
        .mark_rule(color=rule_color)
        .encode(
            opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
            tooltip=tooltip,
        )
        .add_params(nearest)
    )
    upstream_transform = _resolve_layered_transform(chart)
    if upstream_transform is not None:
        rule.transform = list(upstream_transform)

    lines_no_tooltip = alt.layer(
        *[layer.encode(tooltip=alt.value(None)) for layer in chart.layer]
    )
    return alt.layer(lines_no_tooltip, rule)
