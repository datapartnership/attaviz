# Opinionated choropleth maps

Status: approved for implementation

This document defines Attaviz's first opinionated map interface. The module
turns an already joined GeoDataFrame into a publication-ready choropleth while
hiding CRS, classification, missing-data, legend, tooltip, and projection
plumbing behind a small interface.

## Governing decisions

- Callers enable the Attaviz theme explicitly with `attaviz.enable()`.
- Geometry and values arrive already joined in one GeoDataFrame. Attaviz never
  joins or aggregates geographic data silently.
- Attaviz never bundles boundary datasets. Boundary selection, disputed areas,
  and World Bank boundary policy remain the caller's responsibility.
- The factory returns an ordinary Altair chart and never mutates its input.
- The initial implementation supports polygon and multipolygon choropleths.
- GeoPandas is installed through an optional `maps` extra.
- Natural breaks, basemaps, navigation, and other non-native capabilities stay
  outside the initial interface.

## Optional dependency

Add the optional dependency without changing the core installation:

```toml
[project.optional-dependencies]
maps = ["geopandas>=1.0"]
```

Users install map support with:

```bash
pip install "attaviz[maps]"
# or
uv add "attaviz[maps]"
```

Calling a map function without GeoPandas installed raises an actionable error:

```text
choropleth() requires the 'maps' extra: pip install "attaviz[maps]"
```

## Public interface

### Choropleth

```python
attaviz.choropleth(
    geodata,
    *,
    value,
    label,
    value_label=None,
    title=None,
    subtitle=None,
    meaning="neutral",
    classification="continuous",
    classes=5,
    breaks=None,
    domain=None,
    palette=None,
    highlight=None,
    tooltip=None,
    value_format="auto",
    currency=None,
    projection="equalEarth",
    width=600,
    height=400,
)
```

Required semantic fields are keyword-only column names, not Altair shorthand.
The active GeoDataFrame geometry column supplies the shapes.

### Data contract

- `geodata` must be a non-empty GeoPandas GeoDataFrame.
- Its active geometry must contain only `Polygon` or `MultiPolygon` values.
- Missing, empty, or invalid geometry raises `ValueError` naming the affected
  labels.
- A known non-WGS84 CRS is reprojected on a copy to EPSG:4326.
- Missing CRS raises `ValueError`; coordinates are never guessed.
- `value` must exist and be numeric.
- `label` must exist, contain no missing values, and uniquely identify rows.
- Duplicate labels raise `ValueError`; callers dissolve multipart records
  before charting.
- Infinite values raise `ValueError`.
- Missing values remain on the map and render as `attaviz.NO_DATA`.
- Input rows and geometry remain unchanged.

### Content and tooltips

- `label` is always the first tooltip field.
- `value` is always the second tooltip field and uses the selected format.
- Missing values display `No data` rather than `nan` or an empty tooltip.
- `value_label` supplies the legend and value-tooltip heading.
- If omitted, `value_label` humanizes the column name: `poverty_rate` becomes
  `Poverty rate`.
- `tooltip` accepts a sequence of additional column names. Missing names raise
  `ValueError`; headings are humanized.
- `title` and `subtitle` follow the existing factory convention. A subtitle
  without a title raises `ValueError`.

## Color meaning

`meaning` selects an accessible semantic palette:

| Meaning | Palette | Intended use |
|---|---|---|
| `"neutral"` | `SEQ_BLUE` | magnitude without good/bad semantics |
| `"higher_is_better"` | `SEQ_BAD_TO_GOOD` | larger values indicate improvement |
| `"higher_is_worse"` | `SEQ_GOOD_TO_BAD` | larger values indicate deterioration |
| `"change"` | `DIV_DEFAULT` | negative-to-positive change around zero |

`palette` accepts an explicit sequence of CSS colors and overrides the selected
semantic palette. An empty palette or invalid color count raises `ValueError`.

- Sequential meanings containing both negative and positive values emit
  `UserWarning` suggesting `meaning="change"`.
- `meaning="change"` with values on only one side of zero emits `UserWarning`
  suggesting a sequential meaning.
- Change maps use a zero midpoint.
- Without a custom domain, change maps use the symmetric extent
  `(-max(abs(value)), max(abs(value)))`.

## Classification

`classification` accepts four values:

### Continuous

```python
classification="continuous"
```

This is the default. It uses a continuous linear color scale and preserves
differences between neighboring regions.

### Equal interval

```python
classification="equal_interval", classes=5
```

This uses Vega-Lite's `quantize` scale to split the value domain into equal
width ranges.

### Quantile

```python
classification="quantile", classes=5
```

This uses Vega-Lite's `quantile` scale to place approximately equal numbers of
regions in each class.

### Custom thresholds

```python
classification="custom", breaks=[0.1, 0.2, 0.3, 0.5]
```

This uses Vega-Lite's `threshold` scale. `n` thresholds produce `n + 1`
colors.

Classification rules:

- `classes` applies only to `equal_interval` and `quantile`.
- `breaks` applies only to `custom`.
- Custom breaks are numeric, finite, strictly increasing, and fall within the
  effective domain.
- `custom` requires at least one break.
- `classes` must be at least two and cannot exceed the number of distinct
  non-missing values or available palette colors.
- Continuous classification uses the full palette.
- Stepped classifications select exactly the required number of colors,
  distributed across the palette.
- Natural/Jenks and rounded breaks are deferred because Vega-Lite does not
  provide them natively.

## Domain

`domain` is either `None` or a numeric `(minimum, maximum)` tuple.

- The minimum must be strictly less than the maximum.
- Both values must be finite.
- A custom domain that excludes an observed non-missing value raises
  `ValueError`; Attaviz never clips values silently.
- For `meaning="change"`, a custom domain must include zero. It may be
  asymmetric when the caller specifies it explicitly.

## Highlighting and appearance

`highlight` accepts one label or a sequence of labels.

- Unknown labels raise `ValueError`.
- Highlighting changes region borders, not data colors or scale membership.
- Highlighted regions use the selection color and a stronger stroke.
- Non-highlighted regions retain normal WBG geoshape borders.
- Region ordering ensures highlighted boundaries remain visible.
- Missing regions use `NO_DATA` and remain interactive.
- The legend uses the Attaviz bottom placement and selected value format.

## Projection and sizing

- `projection` accepts a Vega-Lite projection name and defaults to
  `"equalEarth"`.
- Vega-Lite fits the projection to the supplied geometry.
- The deterministic default size is `600 × 400` pixels.
- Positive numeric `width` and `height` values are accepted.
- `width="responsive"` remains available explicitly for compatible web
  containers and maps internally to Vega-Lite's container width.
- Framing a responsive map follows the existing `frame()` behavior and resolves
  it to the theme's numeric publication width.

## Map annotation

```python
attaviz.add_map_annotation(
    chart,
    *,
    longitude,
    latitude,
    text,
    position="above",
    offset=8,
    marker=True,
)
```

- Coordinates are finite WGS84 longitude and latitude values.
- Longitude must fall within `[-180, 180]`; latitude within `[-90, 90]`.
- `position` accepts `"above"`, `"below"`, `"left"`, or `"right"`.
- `offset` is a non-negative pixel distance from the anchor.
- `marker=True` renders a small reference-colored anchor point.
- Text may contain newlines.
- Coordinates outside the GeoDataFrame's bounds emit `UserWarning`.
- Callers add multiple annotations by invoking the helper repeatedly.
- The helper uses the choropleth's existing projection and returns an ordinary
  Altair layered chart.

## Formatting

`value_format` follows the existing chart-factory convention:

- `"auto"`
- `"integer"`
- `"decimal"`
- `"percent"`
- `"currency"`
- a D3 number format string

Selecting `"currency"` requires an ISO 4217 `currency` code. Supplying a
currency code with another format raises `ValueError`.

## Warnings and performance

Use ordinary `TypeError` and `ValueError` when the map cannot be interpreted
safely. Use `UserWarning` when it remains valid but deserves attention.

Warnings include:

- sequential data crossing zero;
- change data lying only on one side of zero;
- annotation coordinates outside geometry bounds; and
- more than 5,000 polygons, because embedded GeoJSON may become slow or large.

No warning is emitted for missing values because rendering them explicitly as
`NO_DATA` is normal choropleth behavior.

## Documentation guidance

The choropleth reference must prominently explain that area-based color maps
usually require rates, shares, densities, or normalized indices. Raw totals
often reflect region size or population rather than the phenomenon of interest.
Attaviz documents this rule but does not infer it from unreliable field names.

The gallery uses small local or packaged geometry. Documentation rendering
must not depend on a remote boundary service.

## Implementation order

1. Add the optional `maps` dependency and import guard. Completion: core
   Attaviz imports without GeoPandas, while map calls produce the actionable
   installation error.
2. Implement GeoDataFrame validation and copied reprojection. Completion: CRS,
   geometry type, validity, emptiness, labels, numeric values, infinities, and
   non-mutation are covered by runnable tests.
3. Implement continuous semantic coloring, missing regions, tooltips,
   highlighting, projection, and dimensions. Completion: a framed map with
   missing and highlighted regions serializes and exports correctly.
4. Implement equal-interval, quantile, and custom threshold classifications.
   Completion: each produces the documented Vega-Lite scale and rejects every
   invalid parameter combination.
5. Implement `add_map_annotation()`. Completion: all four positions, optional
   marker, bounds warning, and repeated composition work on choropleth output.
6. Update installation, quickstart, map reference, and gallery documentation.
   Completion: continuous, quantile, custom-break, change, missing-data,
   highlighted, annotated, and framed maps are demonstrated without remote
   boundary dependencies.

Each implementation step includes the smallest runnable tests covering its
non-trivial branches. Documentation and gallery work are part of feature
completion, not a later follow-up.

## Release acceptance

- A basic choropleth takes roughly 8–12 readable lines.
- No CRS conversion, missing-color layer, scale classification, tooltip, or
  projection plumbing is required from callers.
- Invalid or ambiguous geometry fails with affected region labels.
- Missing values remain visible and understandable.
- Continuous and stepped legends match their classifications and formats.
- Highlights preserve the data scale.
- Map annotations use geographic coordinates and the existing projection.
- Input GeoDataFrames remain unchanged.
- HTML and static exports render at the intended dimensions.
- `frame()` metadata aligns with the map title.
- The gallery and documentation demonstrate the entire public interface.

## Non-goals

- Built-in boundary data or automatic boundary downloads.
- Automatic tabular-to-geometry joins.
- Natural/Jenks or rounded classifications.
- Categorical choropleths.
- Pattern fills.
- Automatic polygon labels or collision avoidance.
- Insets or small-multiple maps.
- Tile basemaps, pan, zoom, clustering, routes, flows, and raster layers.
