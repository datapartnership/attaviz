"""Opinionated choropleth maps."""

from __future__ import annotations

import math
import warnings
from collections.abc import Sequence
from typing import Literal

import altair as alt
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

from . import colors
from .charts import _format, _title, _width

_MEANINGS = {
    "neutral": colors.SEQ_BLUE,
    "higher_is_better": colors.SEQ_BAD_TO_GOOD,
    "higher_is_worse": colors.SEQ_GOOD_TO_BAD,
    "change": colors.DIV_DEFAULT,
}
_CLASSIFICATIONS = {"continuous", "equal_interval", "quantile", "custom"}
_POSITIONS = {
    "above": (0, -1, "center", "bottom"),
    "below": (0, 1, "center", "top"),
    "left": (-1, 0, "right", "middle"),
    "right": (1, 0, "left", "middle"),
}


def _geopandas():
    try:
        import geopandas as gpd
    except ImportError as exc:  # pragma: no cover - exercised without the maps extra
        raise ImportError(
            "choropleth() requires the 'maps' extra: pip install \"attaviz[maps]\""
        ) from exc
    return gpd


def _humanize(field: str) -> str:
    return field.replace("_", " ").strip().capitalize()


def _map_data(geodata, value: str, label: str):
    gpd = _geopandas()
    from shapely.geometry import MultiPolygon
    from shapely.geometry.polygon import orient

    if not isinstance(geodata, gpd.GeoDataFrame):
        raise TypeError("geodata must be a GeoPandas GeoDataFrame")
    if geodata.empty:
        raise ValueError("geodata must contain at least one row")
    missing = [field for field in (value, label) if field not in geodata]
    if missing:
        raise ValueError(f"geodata is missing column(s): {', '.join(missing)}")
    if geodata.crs is None:
        raise ValueError("geodata must have a known CRS")
    if not is_numeric_dtype(geodata[value]):
        raise TypeError(f"column {value!r} must be numeric")
    if geodata[label].isna().any():
        raise ValueError(f"label column {label!r} must not contain missing values")
    duplicates = geodata[label].duplicated(keep=False)
    if duplicates.any():
        values = geodata.loc[duplicates, label].drop_duplicates().tolist()
        raise ValueError(f"label values must be unique; duplicates: {values}")

    geometry = geodata.geometry
    bad_geometry = geometry.isna() | geometry.is_empty | ~geometry.is_valid
    bad_type = ~geometry.geom_type.isin(["Polygon", "MultiPolygon"])
    if (bad_geometry | bad_type).any():
        labels = geodata.loc[bad_geometry | bad_type, label].tolist()
        raise ValueError(f"invalid polygon geometry for label(s): {labels}")
    finite = geodata[value].dropna().map(math.isfinite)
    if not finite.all():
        labels = geodata.loc[finite.index[~finite], label].tolist()
        raise ValueError(f"infinite values for label(s): {labels}")

    source = geodata.copy()
    if source.crs.to_epsg() != 4326:
        source = source.to_crs(4326)
    source.geometry = source.geometry.map(
        lambda geometry: (
            orient(geometry, sign=-1.0)
            if geometry.geom_type == "Polygon"
            else MultiPolygon([orient(part, sign=-1.0) for part in geometry.geoms])
        )
    )
    if len(source) > 5_000:
        warnings.warn(
            "choropleth contains more than 5,000 polygons; embedded GeoJSON may be slow",
            UserWarning,
            stacklevel=3,
        )
    return source


def _domain(values: pd.Series, domain, meaning: str) -> list[float]:
    observed = values.dropna()
    if domain is not None:
        if (
            not isinstance(domain, Sequence)
            or isinstance(domain, str)
            or len(domain) != 2
        ):
            raise ValueError("domain must be a (minimum, maximum) pair")
        result = [float(domain[0]), float(domain[1])]
        if not all(math.isfinite(item) for item in result) or result[0] >= result[1]:
            raise ValueError("domain minimum must be finite and less than maximum")
        if not observed.empty and (
            observed.min() < result[0] or observed.max() > result[1]
        ):
            raise ValueError("domain must include every observed value")
        if meaning == "change" and not result[0] <= 0 <= result[1]:
            raise ValueError("change domain must include zero")
        return result
    if observed.empty:
        return [0.0, 1.0]
    if meaning == "change":
        extent = float(observed.abs().max())
        return [-extent, extent] if extent else [-1.0, 1.0]
    minimum, maximum = float(observed.min()), float(observed.max())
    return [minimum, maximum] if minimum < maximum else [minimum, minimum + 1.0]


def _palette(selected, meaning: str) -> list[str]:
    if meaning not in _MEANINGS:
        raise ValueError(f"meaning must be one of {sorted(_MEANINGS)}")
    result = list(_MEANINGS[meaning] if selected is None else selected)
    if not result:
        raise ValueError("palette must contain at least one color")
    return result


def _sample_palette(palette: list[str], count: int) -> list[str]:
    if count > len(palette):
        raise ValueError("classes cannot exceed available palette colors")
    if count == 1:
        return [palette[len(palette) // 2]]
    return [
        palette[round(index * (len(palette) - 1) / (count - 1))]
        for index in range(count)
    ]


def choropleth(
    geodata,
    *,
    value: str,
    label: str,
    value_label: str | None = None,
    title: str | None = None,
    subtitle: str | None = None,
    meaning: str = "neutral",
    classification: str = "continuous",
    classes: int = 5,
    breaks: Sequence[float] | None = None,
    domain: Sequence[float] | None = None,
    palette: Sequence[str] | None = None,
    highlight=None,
    tooltip: Sequence[str] | None = None,
    value_format: str = "auto",
    currency: str | None = None,
    projection: str = "equalEarth",
    width: int | Literal["responsive"] = 600,
    height: int = 400,
) -> alt.Chart:
    """Create a publication-ready polygon choropleth."""
    source = _map_data(geodata, value, label)
    if classification not in _CLASSIFICATIONS:
        raise ValueError(f"classification must be one of {sorted(_CLASSIFICATIONS)}")
    if classification not in {"equal_interval", "quantile"} and classes != 5:
        raise ValueError("classes may only be used with equal_interval or quantile")
    if not isinstance(height, int) or height <= 0:
        raise ValueError("height must be a positive integer")
    extras = list(tooltip or [])
    missing = [field for field in extras if field not in source]
    if missing:
        raise ValueError(f"geodata is missing tooltip column(s): {', '.join(missing)}")

    values = source[value].dropna()
    if meaning != "change" and not values.empty and values.min() < 0 < values.max():
        warnings.warn(
            'data crosses zero; consider meaning="change"', UserWarning, stacklevel=2
        )
    if (
        meaning == "change"
        and not values.empty
        and not (values.min() < 0 < values.max())
    ):
        warnings.warn(
            "change data lies on only one side of zero", UserWarning, stacklevel=2
        )

    selected_palette = _palette(palette, meaning)
    effective_domain = _domain(source[value], domain, meaning)
    distinct = source[value].nunique(dropna=True)
    if classification in {"equal_interval", "quantile"}:
        if not isinstance(classes, int) or classes < 2:
            raise ValueError("classes must be an integer of at least two")
        if classes > distinct:
            raise ValueError("classes cannot exceed distinct non-missing values")
        scale = alt.Scale(
            type="quantize" if classification == "equal_interval" else "quantile",
            domain=effective_domain,
            range=_sample_palette(selected_palette, classes),
        )
        if breaks is not None:
            raise ValueError("breaks may only be used with custom classification")
    elif classification == "custom":
        if not breaks:
            raise ValueError("custom classification requires breaks")
        thresholds = [float(item) for item in breaks]
        if not all(math.isfinite(item) for item in thresholds):
            raise ValueError("breaks must be finite")
        if any(left >= right for left, right in zip(thresholds, thresholds[1:])):
            raise ValueError("breaks must be strictly increasing")
        if thresholds[0] < effective_domain[0] or thresholds[-1] > effective_domain[1]:
            raise ValueError("breaks must fall within the effective domain")
        scale = alt.Scale(
            type="threshold",
            domain=thresholds,
            range=_sample_palette(selected_palette, len(thresholds) + 1),
        )
    else:
        if breaks is not None:
            raise ValueError("breaks may only be used with custom classification")
        scale = alt.Scale(
            type="linear",
            domain=effective_domain,
            domainMid=0 if meaning == "change" else alt.Undefined,
            range=selected_palette,
        )

    selected = (
        []
        if highlight is None
        else ([highlight] if isinstance(highlight, str) else list(highlight))
    )
    unknown = [item for item in selected if item not in set(source[label])]
    if unknown:
        raise ValueError(f"unknown highlight value(s) for {label!r}: {unknown}")

    formatted, axis, formatted_tooltip, _, formatted_field = _format(
        source, value, value_format, currency
    )
    formatted.loc[formatted[value].isna(), formatted_field] = "No data"
    value_title = value_label or _humanize(value)
    formatted_tooltip.title = value_title
    tooltips = [
        alt.Tooltip(label, type="nominal", title=_humanize(label)),
        formatted_tooltip,
    ]
    for field in extras:
        field_type = (
            "quantitative"
            if is_numeric_dtype(formatted[field])
            else "temporal"
            if is_datetime64_any_dtype(formatted[field])
            else "nominal"
        )
        tooltips.append(alt.Tooltip(field, type=field_type, title=_humanize(field)))
    axis_spec = axis.to_dict()
    legend_options = {
        key: axis_spec[key] for key in ("format", "labelExpr") if key in axis_spec
    }
    if classification == "custom":
        legend_options["values"] = thresholds
        legend_options["type"] = "symbol"
    elif classification != "continuous":
        legend_options["type"] = "symbol"
        if value_format == "auto":
            legend_options.pop("labelExpr", None)
        elif value_format == "currency":
            legend_options["labelExpr"] = f"{currency!r} + ' ' + datum.label"
    legend = alt.Legend(orient="bottom", **legend_options)
    color = alt.Color(
        value,
        type="quantitative",
        title=value_title,
        scale=scale,
        legend=legend,
    )
    stroke = (
        alt.condition(
            alt.FieldOneOfPredicate(field=label, oneOf=selected),
            alt.value(colors.SELECTION_PRIMARY),
            alt.value("white"),
        )
        if selected
        else alt.value("white")
    )
    stroke_width = (
        alt.condition(
            alt.FieldOneOfPredicate(field=label, oneOf=selected),
            alt.value(2),
            alt.value(0.5),
        )
        if selected
        else alt.value(0.5)
    )
    base = alt.Chart(formatted)
    no_data = base.mark_geoshape(fill=colors.NO_DATA)
    values_layer = (
        base.transform_filter(f"isValid(datum[{value!r}])")
        .mark_geoshape()
        .encode(color=color)
    )
    outlines = base.mark_geoshape(fillOpacity=0).encode(
        stroke=stroke,
        strokeWidth=stroke_width,
        tooltip=tooltips,
    )
    chart = no_data + values_layer + outlines
    props = {"width": _width(width), "height": height}
    title_value = _title(title, subtitle)
    if title_value is not None:
        props["title"] = title_value
    bounds = [float(item) for item in formatted.total_bounds]
    return chart.project(type=projection).properties(
        **props, usermeta={"attaviz": {"map_bounds": bounds}}
    )


def add_map_annotation(
    chart,
    *,
    longitude: float,
    latitude: float,
    text: str,
    position: str = "above",
    offset: float = 8,
    marker: bool = True,
):
    """Add a geographic annotation to an Attaviz choropleth."""
    if not all(math.isfinite(item) for item in (longitude, latitude)):
        raise ValueError("longitude and latitude must be finite")
    if not -180 <= longitude <= 180 or not -90 <= latitude <= 90:
        raise ValueError(
            "longitude must be within [-180, 180] and latitude within [-90, 90]"
        )
    if position not in _POSITIONS:
        raise ValueError(f"position must be one of {sorted(_POSITIONS)}")
    if not isinstance(offset, (int, float)) or offset < 0:
        raise ValueError("offset must be a non-negative number")
    spec = chart.to_dict()
    bounds = spec.get("usermeta", {}).get("attaviz", {}).get("map_bounds")
    if bounds and not (
        bounds[0] <= longitude <= bounds[2] and bounds[1] <= latitude <= bounds[3]
    ):
        warnings.warn(
            "annotation coordinates fall outside the map bounds",
            UserWarning,
            stacklevel=2,
        )
    dx, dy, align, baseline = _POSITIONS[position]
    data = pd.DataFrame(
        {"longitude": [longitude], "latitude": [latitude], "text": [text]}
    )
    anchor = alt.Chart(data).encode(longitude="longitude:Q", latitude="latitude:Q")
    annotation = anchor.mark_text(
        dx=dx * offset,
        dy=dy * offset,
        align=align,
        baseline=baseline,
        color=colors.TEXT,
    ).encode(text="text:N")
    if marker:
        annotation = (
            anchor.mark_point(filled=True, size=35, color=colors.REFERENCE) + annotation
        )
    base = chart.copy(deep=True)
    metadata = base.usermeta
    projection = base.projection
    title = base.title
    base.usermeta = alt.Undefined
    base.projection = alt.Undefined
    base.title = alt.Undefined
    result = base + annotation
    result.usermeta = metadata
    result.projection = projection
    result.title = title
    return result
