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
```

See the [documentation site](https://datapartnership.github.io/attaviz/) for the full gallery and reference.
