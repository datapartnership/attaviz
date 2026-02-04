# altair-theme-wbg

An [Altair](https://altair-viz.github.io/) theme implementing the
[World Bank Group Data Visualization Style Guide](https://worldbank.github.io/data-visualization-style-guide/).

## Installation

```bash
uv add altair-theme-wbg
```

Or with pip:

```bash
pip install altair-theme-wbg
```

For local development:

```bash
git clone https://github.com/farhanreynaldo/altairtheme.git
cd altairtheme
uv sync --dev
```

## Quick Start

```python
import altair as alt
import altair_theme_wbg

# Enable the WBG theme globally
altair_theme_wbg.enable()

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
import altair_theme_wbg

# Default 9-color categorical palette (used automatically)
altair_theme_wbg.CATEGORICAL
# ['#34A7F2', '#FF9800', '#664AB6', '#4EC2C0', '#F3578E',
#  '#081079', '#0C7C68', '#AA0000', '#DDDA21']

# Accessible text variants (higher contrast on white backgrounds)
altair_theme_wbg.CATEGORICAL_TEXT
```

### Sequential

Six sequential palettes are available:

```python
altair_theme_wbg.SEQ_BLUE          # monochrome blue (default)
altair_theme_wbg.SEQ_GREEN         # monochrome green
altair_theme_wbg.SEQ_PURPLE        # monochrome purple
altair_theme_wbg.SEQ_YELLOW        # monochrome yellow
altair_theme_wbg.SEQ_RED           # monochrome red
altair_theme_wbg.SEQ_BAD_TO_GOOD   # warm → cool (higher = better)
altair_theme_wbg.SEQ_GOOD_TO_BAD   # cool → warm (higher = worse)
```

Use them with `alt.Scale(range=...)`:

```python
alt.Chart(data).mark_rect().encode(
    color=alt.Color(
        "value:Q",
        scale=alt.Scale(range=altair_theme_wbg.SEQ_GREEN),
    ),
)
```

### Diverging

Three diverging palettes with a neutral midpoint (`#EFEFEF`):

```python
altair_theme_wbg.DIV_DEFAULT       # red ↔ blue (good/bad connotation)
altair_theme_wbg.DIV_NEUTRAL       # teal ↔ purple (no connotation)
altair_theme_wbg.DIV_ALTERNATIVE   # blue ↔ red (stronger negative emphasis)
```

Use with `domainMid=0` for symmetric diverging scales:

```python
alt.Chart(data).mark_bar().encode(
    color=alt.Color(
        "change:Q",
        scale=alt.Scale(
            range=altair_theme_wbg.DIV_DEFAULT,
            domainMid=0,
        ),
    ),
)
```

### Semantic Palettes

```python
# Regions (dict: region code → hex)
altair_theme_wbg.REGIONS           # {'NAC': '#34A7F2', 'SSF': '#FF9800', ...}
altair_theme_wbg.REGIONS_TEXT      # accessible text variants
altair_theme_wbg.REGIONS_SECONDARY # 4-shade series per region

# Income groups
altair_theme_wbg.INCOME            # {'HIC': '#016B6C', 'UMC': '#73AF48', ...}
altair_theme_wbg.INCOME_LIST       # as ordered list

# Demographics
altair_theme_wbg.GENDER            # {'female': '#FF9800', 'male': '#664AB6', ...}
altair_theme_wbg.URBANIZATION      # {'urban': '#6D88D1', 'rural': '#54AE89'}
altair_theme_wbg.AGE               # 5 colors, youngest → oldest

# Functional
altair_theme_wbg.REFERENCE         # '#8A969F' — reference line color
altair_theme_wbg.NO_DATA           # '#CED4DE' — missing data fill
altair_theme_wbg.TOTAL             # '#163C6C' — total/aggregate color
altair_theme_wbg.SELECTION_PRIMARY # '#0071BC' — interactive selection
```

### Using Semantic Palettes with Explicit Scales

Map region codes to their official WBG colors:

```python
regions = altair_theme_wbg.REGIONS

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
altair_theme_wbg.PILLARS
# {'people': '#F7B841', 'planet': '#07AB50', 'prosperity': '#872C8F',
#  'infrastructure': '#91302F', 'digital': '#5D6472', 'corporate': '#004972'}
```

## Grey Scale

Five greys for chart elements:

```python
altair_theme_wbg.GREY_500  # '#111111' — primary text
altair_theme_wbg.GREY_400  # '#666666' — secondary text
altair_theme_wbg.GREY_300  # '#8A969F' — reference lines
altair_theme_wbg.GREY_200  # '#CED4DE' — grid lines
altair_theme_wbg.GREY_100  # '#EBEEF4' — backgrounds
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
