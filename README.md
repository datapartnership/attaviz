# attaviz

An [Altair](https://altair-viz.github.io/) theme implementing the
[World Bank Group Data Visualization Style Guide](https://worldbank.github.io/data-visualization-style-guide/).

## Installation

```bash
uv add attaviz
```

Or with pip:

```bash
pip install attaviz
```

For local development:

```bash
git clone https://github.com/farhanreynaldo/attaviz.git
cd attaviz
uv sync --dev
```

## Quick Start

```python
import altair as alt
import attaviz

# Enable the WBG theme globally
attaviz.enable()

# All charts now use the WBG theme automatically
chart = alt.Chart(data).mark_bar().encode(
    x="category:N",
    y="value:Q",
    color="category:N",
)
```

## What the Theme Applies

When enabled, every Altair chart automatically gets:

| Element | WBG Specification |
|---------|-------------------|
| **Font** | Open Sans, sans-serif |
| **Title** | 18px, bold, `#111111` |
| **Subtitle** | 15px, regular, `#666666` |
| **Axis labels** | 13px, semibold, `#111111` |
| **Tick labels** | 13px, regular, `#666666` |
| **Grid lines** | `#CED4DE`, 1px, dashed (4 2) |
| **Legend** | 14×14px symbol dots, semibold labels |
| **Categorical colors** | 9-color WBG palette |
| **Sequential colors** | WBG blue ramp (default) |
| **Diverging colors** | WBG default diverging scale |
| **Line marks** | 4px stroke, round caps/joins |
| **Point marks** | 1px white stroke outline |
| **Geo shapes** | 0.3px grey stroke, round joins |

## Using Color Palettes

The package exports all WBG color palettes as Python lists and dictionaries.

### Categorical

```python
import attaviz

# Default 9-color categorical palette (used automatically)
attaviz.CATEGORICAL
# ['#34A7F2', '#FF9800', '#664AB6', '#4EC2C0', '#F3578E',
#  '#081079', '#0C7C68', '#AA0000', '#DDDA21']

# Accessible text variants (higher contrast on white backgrounds)
attaviz.CATEGORICAL_TEXT
```

### Sequential

Six sequential palettes are available:

```python
attaviz.SEQ_BLUE          # monochrome blue (default)
attaviz.SEQ_GREEN         # monochrome green
attaviz.SEQ_PURPLE        # monochrome purple
attaviz.SEQ_YELLOW        # monochrome yellow
attaviz.SEQ_RED           # monochrome red
attaviz.SEQ_BAD_TO_GOOD   # warm → cool (higher = better)
attaviz.SEQ_GOOD_TO_BAD   # cool → warm (higher = worse)
```

Use them with `alt.Scale(range=...)`:

```python
alt.Chart(data).mark_rect().encode(
    color=alt.Color(
        "value:Q",
        scale=alt.Scale(range=attaviz.SEQ_GREEN),
    ),
)
```

### Diverging

Three diverging palettes with a neutral midpoint (`#EFEFEF`):

```python
attaviz.DIV_DEFAULT       # red ↔ blue (good/bad connotation)
attaviz.DIV_NEUTRAL       # teal ↔ purple (no connotation)
attaviz.DIV_ALTERNATIVE   # blue ↔ red (stronger negative emphasis)
```

Use with `domainMid=0` for symmetric diverging scales:

```python
alt.Chart(data).mark_bar().encode(
    color=alt.Color(
        "change:Q",
        scale=alt.Scale(
            range=attaviz.DIV_DEFAULT,
            domainMid=0,
        ),
    ),
)
```

### Semantic Palettes

```python
# Regions (dict: region code → hex)
attaviz.REGIONS           # {'NAC': '#34A7F2', 'SSF': '#FF9800', ...}
attaviz.REGIONS_TEXT      # accessible text variants
attaviz.REGIONS_SECONDARY # 4-shade series per region

# Income groups
attaviz.INCOME            # {'HIC': '#016B6C', 'UMC': '#73AF48', ...}
attaviz.INCOME_LIST       # as ordered list

# Demographics
attaviz.GENDER            # {'female': '#FF9800', 'male': '#664AB6', ...}
attaviz.URBANIZATION      # {'urban': '#6D88D1', 'rural': '#54AE89'}
attaviz.AGE               # 5 colors, youngest → oldest

# Functional
attaviz.REFERENCE         # '#8A969F' — reference line color
attaviz.NO_DATA           # '#CED4DE' — missing data fill
attaviz.TOTAL             # '#163C6C' — total/aggregate color
attaviz.SELECTION_PRIMARY # '#0071BC' — interactive selection
```

### Using Semantic Palettes with Explicit Scales

Map region codes to their official WBG colors:

```python
regions = attaviz.REGIONS

alt.Chart(data).mark_bar().encode(
    color=alt.Color(
        "region:N",
        scale=alt.Scale(
            domain=list(regions.keys()),
            range=list(regions.values()),
        ),
    ),
)
```

## Pillar Colors

The WBG institutional pillar colors:

```python
attaviz.PILLARS
# {'people': '#F7B841', 'planet': '#07AB50', 'prosperity': '#872C8F',
#  'infrastructure': '#91302F', 'digital': '#5D6472', 'corporate': '#004972'}
```

## Grey Scale

Five greys for chart elements:

```python
attaviz.GREY_500  # '#111111' — primary text
attaviz.GREY_400  # '#666666' — secondary text
attaviz.GREY_300  # '#8A969F' — reference lines
attaviz.GREY_200  # '#CED4DE' — grid lines
attaviz.GREY_100  # '#EBEEF4' — backgrounds
```

## Examples

See [`examples/gallery.ipynb`](examples/gallery.ipynb) for a full gallery including:

1. **Bar chart** — country comparison
2. **Grouped bar chart** — categorical palette
3. **Line chart** — temporal trends
4. **Scatter plot** — two-variable relationships
5. **Stacked area chart** — composition over time
6. **Heatmap** — sequential color scale
7. **Histogram** — distributions
8. **Custom sequential palette** — overriding defaults
9. **Diverging color scale** — centered at zero
10. **Faceted small multiples** — header typography
11. **Color palette reference** — visual swatches

Run the notebook:

```bash
uv run jupyter notebook examples/gallery.ipynb
```

## Reference

- [WBG Data Visualization Style Guide](https://wbg-vis-design.vercel.app/)
- [Altair Documentation](https://altair-viz.github.io/)
- [Vega-Lite Configuration](https://vega.github.io/vega-lite/docs/config.html)
