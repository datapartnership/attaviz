# attaviz

An [Altair](https://altair-viz.github.io/) theme implementing the [World Bank Group Data Visualization Style Guide](https://worldbank.github.io/data-visualization-style-guide/).

**Documentation:** <https://datapartnership.github.io/attaviz/>

## Install

```bash
uv add "attaviz @ git+https://github.com/datapartnership/attaviz.git"
# or
pip install "git+https://github.com/datapartnership/attaviz.git"
```

## Quick start

```python
import altair as alt
import attaviz

attaviz.enable()  # every chart now uses the WBG theme

alt.Chart(data).mark_bar().encode(x="category:N", y="value:Q")
```

See the [documentation site](https://datapartnership.github.io/attaviz/) for the full gallery and reference.