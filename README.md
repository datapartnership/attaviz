# Attaviz

Publication-ready Altair themes, chart templates, and choropleth maps based on
the [World Bank Group Data Visualization Style Guide](https://worldbank.github.io/data-visualization-style-guide/).

**Documentation:** <https://datapartnership.github.io/attaviz/>

## Install

```bash
uv add attaviz
# or
pip install attaviz
```

Add the optional `maps` extra for choropleths: `pip install "attaviz[maps]"`.
Add the optional `tables` extra for styled Great Tables: `pip install "attaviz[tables]"`.

## Quick start

```python
import pandas as pd
import attaviz

attaviz.enable()  # every chart now uses the WBG theme

data = pd.DataFrame(
    {"country": ["Indonesia", "Malaysia"], "population": [280, 35]}
)

chart = attaviz.bar(
    data,
    category="country",
    value="population",
    title="Population by country (millions)",
)

chart = attaviz.frame(
    chart,
    description="Population bars for Indonesia (280 million) and Malaysia (35 million).",
    source="Illustrative example data",
)
```

Set titles and subtitles on the chart template; apply `frame()` last for notes,
source, byline, and accessibility metadata. See [formatting examples](https://datapartnership.github.io/attaviz/reference/formatting.html)
for number and date formats in axes and tooltips.

See the [documentation site](https://datapartnership.github.io/attaviz/) for the full gallery and reference.
