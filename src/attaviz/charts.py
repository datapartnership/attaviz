"""Opinionated editorial chart factories and composition helpers."""

from __future__ import annotations

import warnings
from collections.abc import Sequence
from functools import partial
from typing import Literal

import altair as alt
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

from . import colors
from .formatting import d3_date_format, format_number, vega_scale_labelExpr
from .theme import DEFAULT_DIMENSIONS, FONT, FONT_WEIGHT_REGULAR, SPACING, TYPOGRAPHY

_FORMATS = {"auto", "integer", "decimal", "percent", "currency"}
_DATE_FORMATS = {"day", "month", "month_year", "quarter", "year", "fiscal_year"}
_POSITIONS = {"above", "below", "left", "right"}


def _format_integer(value) -> str:
    return f"{value:,.0f}"


def _format_decimal(value) -> str:
    return f"{value:,.1f}"


def _format_percent(value) -> str:
    return format_number(value, percent=True)


def _format_currency(value, currency: str) -> str:
    return f"{currency} {format_number(value)}"


def _dataframe(data: pd.DataFrame) -> pd.DataFrame:
    if not isinstance(data, pd.DataFrame):
        raise TypeError("data must be a pandas DataFrame")
    if data.empty:
        raise ValueError("data must contain at least one row")
    return data.copy()


def _columns(data: pd.DataFrame, *fields: str | None) -> None:
    missing = [field for field in fields if field is not None and field not in data]
    if missing:
        raise ValueError(f"data is missing column(s): {', '.join(missing)}")


def _numeric(data: pd.DataFrame, *fields: str) -> None:
    invalid = [field for field in fields if not is_numeric_dtype(data[field])]
    if invalid:
        raise TypeError(f"column(s) must be numeric: {', '.join(invalid)}")


def _values(value: object | Sequence[object] | None) -> list[object]:
    if value is None:
        return []
    if isinstance(value, str) or not isinstance(value, Sequence):
        return [value]
    return list(value)


def _validate_highlight(
    data: pd.DataFrame, field: str, highlight: object | Sequence[object] | None
) -> list[object]:
    selected = _values(highlight)
    unknown = [value for value in selected if value not in set(data[field].dropna())]
    if unknown:
        raise ValueError(f"unknown highlight value(s) for {field!r}: {unknown}")
    return selected


def _drop_missing(data: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    missing = data[fields].isna().any(axis=1)
    if missing.any():
        warnings.warn(
            f"omitted {int(missing.sum())} row(s) with missing {', '.join(fields)}",
            UserWarning,
            stacklevel=3,
        )
        data = data.loc[~missing].copy()
    if data.empty:
        raise ValueError("no rows remain after removing missing values")
    return data


def _format(
    data: pd.DataFrame,
    field: str,
    selected: str,
    currency: str | None,
) -> tuple[pd.DataFrame, alt.Axis, alt.Tooltip, alt.Text, str]:
    if selected == "currency" and not currency:
        raise ValueError("currency is required when format is 'currency'")
    if currency and selected != "currency":
        raise ValueError("currency may only be used when format is 'currency'")

    label_field = f"__attaviz_{field}_label"
    while label_field in data:
        label_field += "_"

    if selected in _FORMATS:
        if selected == "auto":
            formatter = format_number
            axis = alt.Axis(
                labelExpr=vega_scale_labelExpr(), tickCount=5, labelOverlap="greedy"
            )
        elif selected == "integer":
            formatter = _format_integer
            axis = alt.Axis(format=",.0f", tickCount=5, labelOverlap="greedy")
        elif selected == "decimal":
            formatter = _format_decimal
            axis = alt.Axis(format=",.1f", tickCount=5, labelOverlap="greedy")
        elif selected == "percent":
            formatter = _format_percent
            axis = alt.Axis(format=".1%", tickCount=5, labelOverlap="greedy")
        else:
            formatter = partial(_format_currency, currency=currency)
            axis = alt.Axis(
                labelExpr=f"{currency!r} + ' ' + ({vega_scale_labelExpr()})",
                tickCount=5,
                labelOverlap="greedy",
            )

        data[label_field] = data[field].map(formatter)
        tooltip = alt.Tooltip(label_field, type="nominal", title=field)
        text = alt.Text(label_field, type="nominal")
    else:
        axis = alt.Axis(format=selected, tickCount=5, labelOverlap="greedy")
        tooltip = alt.Tooltip(field, type="quantitative", format=selected)
        text = alt.Text(field, type="quantitative", format=selected)

    return data, axis, tooltip, text, label_field


def _title(title: str | None, subtitle: str | None):
    if title is None:
        if subtitle is not None:
            raise ValueError("subtitle requires title")
        return None
    return (
        alt.Title(title, subtitle=subtitle)
        if subtitle is not None
        else alt.Title(title)
    )


def _properties(chart, *, width, height, title, subtitle):
    properties = {"width": _width(width), "height": height}
    title_value = _title(title, subtitle)
    if title_value is not None:
        properties["title"] = title_value
    return chart.properties(**properties)


def _width(width: int | Literal["responsive"]):
    if width == "responsive":
        return "container"
    if isinstance(width, int) and width > 0:
        return width
    raise ValueError("width must be a positive integer or 'responsive'")


def _height(height: int | None, default: int) -> int:
    if height is None:
        return default
    if isinstance(height, int) and height > 0:
        return height
    raise ValueError("height must be a positive integer")


def _warn_many_series(data: pd.DataFrame, field: str) -> None:
    count = data[field].nunique()
    if count > len(colors.CATEGORICAL):
        warnings.warn(
            f"{count} color series exceed the {len(colors.CATEGORICAL)}-color palette",
            UserWarning,
            stacklevel=3,
        )


def bar(
    data: pd.DataFrame,
    *,
    category: str,
    value: str,
    title: str | None = None,
    subtitle: str | None = None,
    sort: Literal["ascending", "descending", "data"] | Sequence[object] = "descending",
    labels: bool = True,
    highlight: object | Sequence[object] | None = None,
    value_format: str = "auto",
    currency: str | None = None,
    width: int | Literal["responsive"] = "responsive",
    height: int | None = None,
) -> alt.Chart | alt.LayerChart:
    """Create a publication-ready horizontal bar chart."""
    source = _dataframe(data)
    _columns(source, category, value)
    _numeric(source, value)
    source = _drop_missing(source, [category, value])

    duplicates = source[category].duplicated(keep=False)
    if duplicates.any():
        values = source.loc[duplicates, category].drop_duplicates().tolist()
        raise ValueError(f"category values must be unique; duplicates: {values}")

    if len(source) > 20:
        warnings.warn(
            f"bar chart contains {len(source)} categories; consider filtering or grouping",
            UserWarning,
            stacklevel=2,
        )
    if source[category].astype(str).str.len().gt(30).any():
        warnings.warn(
            "category labels longer than 30 characters may be truncated",
            UserWarning,
            stacklevel=2,
        )

    selected = _validate_highlight(source, category, highlight)
    source, axis, tooltip_value, text_value, _ = _format(
        source, value, value_format, currency
    )

    if isinstance(sort, str):
        if sort not in {"ascending", "descending", "data"}:
            raise ValueError(
                "sort must be 'ascending', 'descending', 'data', or a sequence"
            )
        sort_value = {"ascending": "x", "descending": "-x", "data": None}[sort]
    else:
        sort_value = list(sort)
        unknown = [item for item in sort_value if item not in set(source[category])]
        if unknown:
            raise ValueError(f"sort contains unknown category value(s): {unknown}")

    if selected:
        color = alt.condition(
            alt.FieldOneOfPredicate(field=category, oneOf=selected),
            alt.value(colors.CATEGORICAL[0]),
            alt.value(colors.GREY_200),
        )
    else:
        color = alt.value(colors.CATEGORICAL[0])

    base = alt.Chart(source).encode(
        x=alt.X(
            value,
            type="quantitative",
            title=None,
            scale=alt.Scale(zero=True),
            axis=axis,
        ),
        y=alt.Y(
            category,
            type="nominal",
            title=None,
            sort=sort_value,
            axis=alt.Axis(grid=False),
        ),
    )
    bars = base.mark_bar().encode(
        color=color,
        tooltip=[alt.Tooltip(category, type="nominal", title=category), tooltip_value],
    )
    chart = bars
    if labels:
        chart = bars + base.mark_text(align="left", dx=5).encode(text=text_value)

    return _properties(
        chart,
        width=width,
        height=_height(height, max(120, len(source) * 28)),
        title=title,
        subtitle=subtitle,
    )


def _line_x(source: pd.DataFrame, field: str, date_format: str):
    if is_datetime64_any_dtype(source[field]):
        selected = "month_year" if date_format == "auto" else date_format
        fmt = d3_date_format(selected) if selected in _DATE_FORMATS else selected
        return "temporal", alt.Axis(format=fmt), fmt
    if is_numeric_dtype(source[field]):
        return "quantitative", alt.Axis(), None
    raise TypeError(f"line x column {field!r} must be numeric or temporal")


def _single_line_hover(
    chart: alt.Chart | alt.LayerChart,
    source: pd.DataFrame,
    x: str,
    x_type: str,
    y: str,
    tooltip_value: alt.Tooltip,
):
    nearest = alt.selection_point(
        nearest=True, on="pointerover", fields=[x], empty=False
    )
    rule = (
        alt.Chart(source)
        .mark_rule(color=colors.GREY_400)
        .encode(
            x=alt.X(x, type=x_type),
            opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
            tooltip=[alt.Tooltip(x, type=x_type), tooltip_value],
        )
        .add_params(nearest)
    )
    return chart + rule


def line(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    series: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    highlight: object | Sequence[object] | None = None,
    end_labels: bool = True,
    points: bool = False,
    zero: bool = False,
    value_format: str = "auto",
    currency: str | None = None,
    date_format: str = "auto",
    width: int | Literal["responsive"] = "responsive",
    height: int | None = None,
) -> alt.LayerChart:
    """Create a publication-ready single- or multi-series line chart."""
    source = _dataframe(data)
    _columns(source, x, y, series)
    _numeric(source, y)
    required = [x] + ([series] if series else [])
    source = _drop_missing(source, required)
    x_type, x_axis, x_format = _line_x(source, x, date_format)

    keys = [x] + ([series] if series else [])
    duplicates = source.duplicated(keys, keep=False)
    if duplicates.any():
        values = source.loc[duplicates, keys].drop_duplicates().to_dict("records")
        raise ValueError(f"line keys must be unique; duplicates: {values}")
    source = source.sort_values(keys).copy()
    source, y_axis, tooltip_value, _, _ = _format(source, y, value_format, currency)

    selected: list[object] = []
    if highlight is not None:
        if series is None:
            raise ValueError("highlight requires series")
        selected = _validate_highlight(source, series, highlight)

    encoding: dict[str, object] = {
        "x": alt.X(x, type=x_type, title=None, axis=x_axis),
        "y": alt.Y(
            y, type="quantitative", title=y, scale=alt.Scale(zero=zero), axis=y_axis
        ),
    }
    if series:
        _warn_many_series(source, series)
        show_end_labels = end_labels and source[series].nunique() <= 5
        encoding["color"] = alt.Color(
            series,
            type="nominal",
            title=None,
            legend=None if show_end_labels else alt.Undefined,
        )
        encoding["tooltip"] = tooltip_value
        if selected:
            encoding["opacity"] = alt.condition(
                alt.FieldOneOfPredicate(field=series, oneOf=selected),
                alt.value(1),
                alt.value(0.18),
            )

    main = alt.Chart(source).mark_line().encode(**encoding)
    point_marks = alt.Chart(source).mark_point().encode(**encoding)

    if series:
        from .interactions import add_hover

        marks: alt.Chart | alt.LayerChart = add_hover(main, x=x, x_format=x_format)
        if points:
            marks = marks + point_marks
        if show_end_labels:
            ends = (
                source.dropna(subset=[y])
                .sort_values(x)
                .groupby(series, as_index=False)
                .tail(1)
            )
            labels = (
                alt.Chart(ends)
                .mark_text(align="left", dx=8)
                .encode(
                    x=alt.X(x, type=x_type),
                    y=alt.Y(y, type="quantitative"),
                    text=alt.Text(series, type="nominal"),
                    color=alt.Color(series, type="nominal", legend=None),
                    opacity=(
                        alt.condition(
                            alt.FieldOneOfPredicate(field=series, oneOf=selected),
                            alt.value(1),
                            alt.value(0.18),
                        )
                        if selected
                        else alt.value(1)
                    ),
                )
            )
            marks = marks + labels
    else:
        marks = main + point_marks if points else main
        marks = _single_line_hover(marks, source, x, x_type, y, tooltip_value)

    return _properties(
        marks,
        width=width,
        height=_height(height, 360),
        title=title,
        subtitle=subtitle,
    )


def scatter(
    data: pd.DataFrame,
    *,
    x: str,
    y: str,
    label: str | None = None,
    series: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    highlight: object | Sequence[object] | None = None,
    x_zero: bool = False,
    y_zero: bool = False,
    x_format: str = "auto",
    x_currency: str | None = None,
    y_format: str = "auto",
    y_currency: str | None = None,
    width: int | Literal["responsive"] = "responsive",
    height: int | None = None,
) -> alt.Chart | alt.LayerChart:
    """Create a publication-ready scatter chart."""
    source = _dataframe(data)
    _columns(source, x, y, label, series)
    _numeric(source, x, y)
    source = _drop_missing(source, [x, y])
    source, x_axis, x_tooltip, _, _ = _format(source, x, x_format, x_currency)
    source, y_axis, y_tooltip, _, _ = _format(source, y, y_format, y_currency)

    selected: list[object] = []
    if highlight is not None:
        if label is None:
            raise ValueError("highlight requires label")
        selected = _validate_highlight(source, label, highlight)

    encoding: dict[str, object] = {
        "x": alt.X(
            x, type="quantitative", title=x, scale=alt.Scale(zero=x_zero), axis=x_axis
        ),
        "y": alt.Y(
            y, type="quantitative", title=y, scale=alt.Scale(zero=y_zero), axis=y_axis
        ),
    }
    if series:
        _warn_many_series(source, series)
        encoding["color"] = alt.Color(series, type="nominal", title=None)
    else:
        encoding["color"] = alt.value(colors.CATEGORICAL[0])
    if selected:
        encoding["opacity"] = alt.condition(
            alt.FieldOneOfPredicate(field=label, oneOf=selected),
            alt.value(1),
            alt.value(0.18),
        )

    tooltips: list[alt.Tooltip] = []
    if label:
        tooltips.append(alt.Tooltip(label, type="nominal", title=label))
    if series and series != label:
        tooltips.append(alt.Tooltip(series, type="nominal", title=series))
    tooltips.extend([x_tooltip, y_tooltip])

    points = alt.Chart(source).mark_circle(size=80).encode(**encoding, tooltip=tooltips)
    chart: alt.Chart | alt.LayerChart = points
    if selected and label:
        highlighted_points = points.transform_filter(
            alt.FieldOneOfPredicate(field=label, oneOf=selected)
        )
        labels = (
            alt.Chart(source)
            .transform_filter(alt.FieldOneOfPredicate(field=label, oneOf=selected))
            .mark_text(align="left", dx=8, dy=-8)
            .encode(
                x=alt.X(x, type="quantitative"),
                y=alt.Y(y, type="quantitative"),
                text=alt.Text(label, type="nominal"),
                color=alt.value(colors.TEXT),
            )
        )
        chart = points + highlighted_points + labels

    return _properties(
        chart,
        width=width,
        height=_height(height, 360),
        title=title,
        subtitle=subtitle,
    )


def _leaf_charts(chart, inherited_data=alt.Undefined):
    data = getattr(chart, "data", alt.Undefined)
    if data is alt.Undefined:
        data = inherited_data
    layers = getattr(chart, "layer", alt.Undefined)
    if layers is not alt.Undefined:
        for layer in layers:
            yield from _leaf_charts(layer, data)
    else:
        yield chart, data


def _chart_context(chart):
    contexts = {}
    for leaf, data in _leaf_charts(chart):
        encoding = getattr(leaf, "encoding", alt.Undefined)
        if encoding is alt.Undefined or not isinstance(data, pd.DataFrame):
            continue
        x = getattr(encoding, "x", alt.Undefined)
        y = getattr(encoding, "y", alt.Undefined)
        if x is alt.Undefined or y is alt.Undefined:
            continue
        x_dict, y_dict = x.to_dict(), y.to_dict()
        if "field" in x_dict and "field" in y_dict:
            key = (x_dict["field"], y_dict["field"])
            contexts.setdefault(key, (data, x_dict, y_dict))
    if len(contexts) == 1:
        return next(iter(contexts.values()))
    if len(contexts) > 1:
        raise TypeError("helper requires an unambiguous pair of x and y fields")
    raise TypeError("helper requires a chart with in-memory x and y field encodings")


def _outside(value, series: pd.Series) -> bool:
    values = series.dropna()
    return not values.empty and (value < values.min() or value > values.max())


def add_annotation(
    chart,
    *,
    x,
    y,
    text: str,
    position: Literal["above", "below", "left", "right"] = "above",
    offset: int = 8,
    marker: bool = True,
):
    """Add text anchored to a data coordinate."""
    if position not in _POSITIONS:
        raise ValueError(f"position must be one of {sorted(_POSITIONS)}")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    data, x_enc, y_enc = _chart_context(chart)
    if _outside(x, data[x_enc["field"]]) or _outside(y, data[y_enc["field"]]):
        warnings.warn(
            "annotation lies outside the observed domain", UserWarning, stacklevel=2
        )

    annotation = pd.DataFrame(
        {x_enc["field"]: [x], y_enc["field"]: [y], "text": [text]}
    )
    anchor = alt.Chart(annotation).encode(
        x=alt.X(x_enc["field"], type=x_enc.get("type")),
        y=alt.Y(y_enc["field"], type=y_enc.get("type")),
    )
    settings = {
        "above": ("center", "bottom", 0, -offset),
        "below": ("center", "top", 0, offset),
        "left": ("right", "middle", -offset, 0),
        "right": ("left", "middle", offset, 0),
    }
    align, baseline, dx, dy = settings[position]
    label = anchor.mark_text(align=align, baseline=baseline, dx=dx, dy=dy).encode(
        text=alt.Text("text:N")
    )
    layers = [chart]
    if marker:
        layers.append(anchor.mark_point(size=45, color=colors.REFERENCE))
    layers.append(label)
    return alt.layer(*layers)


def add_reference_line(
    chart,
    *,
    value,
    axis: Literal["x", "y"] = "y",
    label: str | None = None,
):
    """Add a labeled reference line to an x or y axis."""
    if axis not in {"x", "y"}:
        raise ValueError("axis must be 'x' or 'y'")
    data, x_enc, y_enc = _chart_context(chart)
    encoding = x_enc if axis == "x" else y_enc
    field = encoding["field"]
    if _outside(value, data[field]):
        warnings.warn(
            "reference line lies outside the observed domain", UserWarning, stacklevel=2
        )
    reference = pd.DataFrame({field: [value], "label": [label or ""]})
    base = alt.Chart(reference).encode(
        **{
            axis: alt.X(field, type=encoding.get("type"))
            if axis == "x"
            else alt.Y(field, type=encoding.get("type"))
        }
    )
    line_mark = base.mark_rule(color=colors.REFERENCE, strokeDash=[4, 3])
    if not label:
        return chart + line_mark
    text = base.mark_text(
        align="left" if axis == "y" else "center",
        baseline="bottom",
        dx=5 if axis == "y" else 0,
        dy=-5 if axis == "x" else 0,
        color=colors.TEXT_SUBTLE,
    ).encode(text="label:N")
    return chart + line_mark + text


def add_reference_range(
    chart,
    *,
    start,
    end,
    axis: Literal["x", "y"] = "y",
    label: str | None = None,
):
    """Add a labeled reference band to an x or y axis."""
    if axis not in {"x", "y"}:
        raise ValueError("axis must be 'x' or 'y'")
    if start > end:
        raise ValueError("reference range start must not exceed end")
    data, x_enc, y_enc = _chart_context(chart)
    encoding = x_enc if axis == "x" else y_enc
    field, end_field = encoding["field"], "__attaviz_range_end"
    if _outside(start, data[field]) or _outside(end, data[field]):
        warnings.warn(
            "reference range lies outside the observed domain",
            UserWarning,
            stacklevel=2,
        )
    reference = pd.DataFrame({field: [start], end_field: [end], "label": [label or ""]})
    channel = (
        {"x": alt.X(field, type=encoding.get("type")), "x2": alt.X2(end_field)}
        if axis == "x"
        else {"y": alt.Y(field, type=encoding.get("type")), "y2": alt.Y2(end_field)}
    )
    base = alt.Chart(reference).encode(**channel)
    band = base.mark_rect(color=colors.REFERENCE, opacity=0.14)
    if not label:
        return band + chart
    text = base.mark_text(
        align="left",
        baseline="bottom",
        color=colors.TEXT_SUBTLE,
    ).encode(text="label:N")
    return band + chart + text


def frame(
    chart,
    *,
    description: str,
    source: str | None = None,
    source_url: str | None = None,
    note: str | None = None,
    byline: str | None = None,
):
    """Add accessible publication metadata around a completed chart."""
    if not description.strip():
        raise ValueError("description must not be empty")
    if source_url and not source:
        raise ValueError("source_url requires source")

    rows: list[str] = []
    if note:
        rows.append(f"Note: {note}")
    if source:
        rows.append(f"Source: {source}")
    if byline:
        rows.append(f"By: {byline}")

    chart = chart.copy(deep=True)
    existing_meta = getattr(chart, "usermeta", alt.Undefined)
    metadata = {} if existing_meta is alt.Undefined else dict(existing_meta)
    chart.usermeta = alt.Undefined

    if getattr(chart, "width", alt.Undefined) == "container":
        chart = chart.properties(width=DEFAULT_DIMENSIONS["medium"][0])

    if source_url:
        metadata.setdefault("attaviz", {})["source_url"] = source_url

    result = alt.vconcat(chart, spacing=SPACING["medium"]["xs"]).properties(
        description=description,
        usermeta=metadata,
    )
    if not rows:
        return result

    footer = alt.TitleParams(
        text=rows,
        orient="bottom",
        anchor="start",
        frame="bounds",
        font=FONT,
        fontSize=TYPOGRAPHY["medium"]["S"],
        fontWeight=FONT_WEIGHT_REGULAR,
        color=colors.TEXT_SUBTLE,
        lineHeight=round(TYPOGRAPHY["medium"]["S"] * 1.5),
        offset=SPACING["medium"]["m"],
    )
    return result.properties(title=footer)
