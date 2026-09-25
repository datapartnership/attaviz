# Opinionated chart factories

Status: approved for implementation

This document defines Attaviz's first opinionated chart interface. The goal is
to produce publication-ready editorial charts from a pandas DataFrame and a few
semantic field names while preserving ordinary Altair chart objects.

## Governing decisions

- Callers enable the Attaviz theme explicitly with `attaviz.enable()`.
- Factories return standard Altair chart types and never mutate input data.
- Data mappings are keyword-only and use column names, not Altair shorthand.
- Input data must already be summarized where the chart requires it. Factories
  never aggregate silently.
- Factories expose recurring editorial decisions, not arbitrary Vega-Lite
  options. Advanced customization happens through Altair after construction.
- The first release accepts pandas DataFrames. GeoPandas DataFrames work through
  inheritance.
- No factory accepts `**kwargs`.

## Public interface

### Bar chart

```python
attaviz.bar(
    data,
    *,
    category,
    value,
    title=None,
    subtitle=None,
    sort="descending",
    labels=True,
    highlight=None,
    value_format="auto",
    currency=None,
    width="responsive",
    height=None,
)
```

`bar()` always creates horizontal bars. A future `column()` may provide
vertical bars explicitly; orientation is never guessed.

- Each category must occur exactly once. Duplicate categories raise
  `ValueError`.
- `value` must be numeric.
- Bars start at zero and sort by value descending by default.
- `sort` accepts `"ascending"`, `"descending"`, `"data"`, or an explicit
  category sequence.
- End labels and tooltips share the selected number format.
- `highlight` accepts one category or a sequence. Highlighted bars retain the
  primary color while other bars are muted.
- Unknown highlighted categories raise `ValueError`.
- Missing category or value rows are omitted with `UserWarning`.
- The default height is calculated from the category count to preserve legible
  bar thickness.

Grouped bars, stacked bars, error bars, and automatic aggregation are outside
this interface.

### Line chart

```python
attaviz.line(
    data,
    *,
    x,
    y,
    series=None,
    title=None,
    subtitle=None,
    highlight=None,
    end_labels=True,
    points=False,
    zero=False,
    value_format="auto",
    currency=None,
    date_format="auto",
    width="responsive",
    height=None,
)
```

`series` is the optional column that identifies multiple lines.

- Without `series`, each `x` value must be unique.
- With `series`, each `(x, series)` pair must be unique.
- Duplicate keys raise `ValueError`; the factory never aggregates them.
- Rows are sorted by `x` before rendering.
- Numeric and temporal x fields are inferred from DataFrame dtypes. String
  dates are not coerced automatically.
- Missing y values create gaps. Lines do not connect across missing values.
- The y scale does not include zero unless `zero=True`.
- Hovering displays a shared rule and the values of all visible series.
- `highlight` accepts one series or a sequence; unknown series raise
  `ValueError`.
- End labels replace the legend for up to five series. Above five series,
  Attaviz uses a legend. `end_labels=False` always uses a legend.
- Point markers are hidden unless `points=True`.

Confidence bands, dual axes, interpolation controls, forecasts, rolling
statistics, and mixed mark charts are outside this interface.

### Scatter chart

```python
attaviz.scatter(
    data,
    *,
    x,
    y,
    label=None,
    series=None,
    title=None,
    subtitle=None,
    highlight=None,
    x_zero=False,
    y_zero=False,
    x_format="auto",
    x_currency=None,
    y_format="auto",
    y_currency=None,
    width="responsive",
    height=None,
)
```

- Each row represents an observation. Duplicate coordinates are valid.
- `x` and `y` must be numeric.
- `label` identifies observations in tooltips and supplies text for highlighted
  points.
- `series` optionally groups observations by color.
- `highlight` contains values from `label`; using it without `label` raises
  `ValueError`.
- Highlighted points retain their color, render above muted points, and receive
  direct labels.
- Both axes omit zero by default.
- Missing x or y rows are omitted with `UserWarning`.

Bubble sizing, regression lines, quadrants, marginal distributions, labeling
every point, and automatic statistical claims are outside this interface.

## Publication frame

```python
attaviz.frame(
    chart,
    *,
    description,
    source=None,
    source_url=None,
    note=None,
    byline=None,
)
```

`frame()` is applied last, after chart customization and composition.

- `description` is required and becomes Vega-Lite accessibility metadata. It
  is not displayed as chart text.
- `source`, `note`, and `byline` are optional and render below the chart in a
  consistent order and style.
- `source_url` requires `source`.
- The result remains an ordinary Altair composition that can be displayed or
  exported.
- `add_caption()` remains available for compatibility but is not the preferred
  interface for new publication charts.

Title and subtitle remain factory arguments so a basic chart does not require
a separate framing call during exploration.

## Editorial composition helpers

### Annotation

```python
attaviz.add_annotation(
    chart,
    *,
    x,
    y,
    text,
    position="above",
    offset=8,
    marker=True,
)
```

- `x` and `y` are data coordinates.
- `position` accepts `"above"`, `"below"`, `"left"`, or `"right"`.
- `offset` is the distance from the anchor in pixels.
- `marker=True` renders a small point at the anchor.
- Text may contain newlines.
- Callers add multiple annotations by calling the helper repeatedly.
- An annotation outside the observed domain produces `UserWarning`.

Free-positioned annotations, arrows, circles, and arbitrary styling are outside
the initial interface.

### Reference line

```python
attaviz.add_reference_line(
    chart,
    *,
    value,
    axis="y",
    label=None,
)
```

### Reference range

```python
attaviz.add_reference_range(
    chart,
    *,
    start,
    end,
    axis="y",
    label=None,
)
```

- `axis` must be `"x"` or `"y"`; Attaviz never guesses.
- Reference marks are visually subordinate to the data.
- Labels are optional and use the referenced axis format.
- A range with `start > end` raises `ValueError`.
- A reference outside the observed domain produces `UserWarning`.

## Formatting

Number format arguments accept `"auto"`, `"integer"`, `"decimal"`,
`"percent"`, `"currency"`, or a D3 number format string. Date format arguments
accept `"auto"`, the existing Attaviz date presets, or a D3 date format string.

Selecting `"currency"` requires the corresponding ISO 4217 currency code:

```python
attaviz.bar(
    data,
    category="country",
    value="gdp",
    value_format="currency",
    currency="USD",
)
```

The first release displays the unambiguous code, such as `USD 1.2B`, rather
than assuming a currency symbol or locale. Supplying a currency code when the
format is not `"currency"` raises `ValueError` so unused arguments cannot pass
silently.

## Sizing

`width="responsive"` maps to Vega-Lite's container width and fills the parent
HTML element. Numeric pixel widths remain supported. Callers should provide a
numeric width for deterministic PNG, SVG, or PDF export because static output
has no browser container.

Bar height is data-dependent by default. Line and scatter charts use stable
default heights. An explicit numeric `height` overrides either behavior.
Existing `configure_size()` remains supported for post-construction changes.

Attaviz does not change chart type or editorial layout at mobile breakpoints.
That behavior belongs in a host application rather than these factories.

## Validation policy

Use ordinary `TypeError` and `ValueError` when a chart cannot be interpreted
safely. Use `UserWarning` when the chart remains valid but deserves editorial
attention.

Warnings include:

- more than 20 bars;
- omitted missing values;
- more color series than the categorical palette can distinguish;
- category labels longer than 30 characters; and
- annotations or references outside the observed domain.

The following are normal behavior and do not warn:

- switching from line end labels to a legend above five series;
- sorting line input chronologically;
- muting non-highlighted observations; and
- responsive width adapting to its parent.

## Implementation order

1. Implement `bar()` and the shared validation and formatting behavior it
   requires. Completion: a summarized DataFrame produces a labeled responsive
   bar chart and every documented bar validation case is checked.
2. Implement `line()` using the shared behavior. Completion: single- and
   multi-series charts satisfy uniqueness, gap, hover, highlight, and labeling
   rules.
3. Implement `scatter()`. Completion: grouping, highlighting, tooltips, and
   independent axis formats follow this document.
4. Implement `add_annotation()`, `add_reference_line()`, and
   `add_reference_range()`. Completion: every helper composes with all three
   factory outputs.
5. Implement `frame()`. Completion: accessibility metadata and optional footer
   fields survive HTML and static serialization.
6. Update the public documentation and gallery. Completion: the quickstart
   uses a factory, every new public function has reference documentation, and
   the gallery contains representative bar, line, scatter, annotation,
   reference, highlight, responsive, currency, and framed examples.

Each implementation step includes the smallest runnable tests covering its
non-trivial branches. The release is complete only when the gallery and
documentation in step 6 are updated; they are part of the feature, not a
follow-up release.

## Release acceptance

- A basic publication chart takes roughly 5–10 readable lines.
- Sorting, labels, tooltips, formatting, and responsive sizing require no
  Altair knowledge.
- Invalid or ambiguous data fails with a specific explanation.
- Every returned value remains customizable and serializable through Altair.
- Input DataFrames remain unchanged.
- Static exports are deterministic when given numeric dimensions.
- `frame()` always includes an accessibility description.
- The gallery and documentation demonstrate the complete public interface.

