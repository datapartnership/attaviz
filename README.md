# attaviz

An [Altair](https://altair-viz.github.io/) theme implementing the
[World Bank Group Data Visualization Style
Guide](https://worldbank.github.io/data-visualization-style-guide/).

**Documentation:** <https://farhanreynaldo.github.io/attaviz/>

## Install

```bash
uv add "attaviz @ git+https://github.com/farhanreynaldo/attaviz.git"
# or
pip install "git+https://github.com/farhanreynaldo/attaviz.git"
```

## Quick start

```python
import altair as alt
import attaviz

attaviz.enable()  # every chart now uses the WBG theme

alt.Chart(data).mark_bar().encode(x="category:N", y="value:Q")
```

See the [documentation site](https://farhanreynaldo.github.io/attaviz/)
for the full gallery and reference.

## License

MIT.
