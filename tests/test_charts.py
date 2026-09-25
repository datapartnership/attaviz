import warnings

import pandas as pd
import pytest

import attaviz


@pytest.fixture(autouse=True)
def enable_theme():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        attaviz.enable()


def test_bar_serializes_without_mutating_input():
    data = pd.DataFrame(
        {"country": ["Indonesia", "Malaysia"], "population": [280_000_000, 35_000_000]}
    )
    original = data.copy()

    chart = attaviz.bar(
        data,
        category="country",
        value="population",
        highlight="Indonesia",
        title="Population",
    )

    spec = chart.to_dict()
    assert spec["width"] == "container"
    assert len(spec["layer"]) == 2
    pd.testing.assert_frame_equal(data, original)


def test_bar_requires_summarized_data():
    data = pd.DataFrame({"country": ["A", "A"], "value": [1, 2]})

    with pytest.raises(ValueError, match="must be unique"):
        attaviz.bar(data, category="country", value="value")


def test_currency_requires_code():
    data = pd.DataFrame({"country": ["A"], "value": [1]})

    with pytest.raises(ValueError, match="currency is required"):
        attaviz.bar(
            data,
            category="country",
            value="value",
            value_format="currency",
        )


def test_line_serializes_multi_series_with_points_and_end_labels():
    data = pd.DataFrame(
        {
            "year": pd.to_datetime(["2020-01-01", "2021-01-01"] * 2),
            "country": ["A", "A", "B", "B"],
            "value": [1, 2, 3, 4],
        }
    )

    chart = attaviz.line(
        data,
        x="year",
        y="value",
        series="country",
        points=True,
        highlight="A",
    )

    spec = chart.to_dict()
    assert spec["width"] == "container"
    assert len(spec["layer"]) >= 3
    assert spec["layer"][0]["encoding"]["color"]["legend"] is None


def test_line_serializes_numeric_x_and_uses_selected_hover_format():
    data = pd.DataFrame(
        {
            "year": [2020, 2021, 2020, 2021],
            "country": ["A", "A", "B", "B"],
            "rate": [0.1, 0.2, 0.3, 0.4],
        }
    )

    spec = attaviz.line(
        data,
        x="year",
        y="rate",
        series="country",
        value_format="percent",
    ).to_dict()

    hover = spec["layer"][1]
    assert hover["encoding"]["tooltip"][0] == {
        "field": "year",
        "type": "quantitative",
    }
    assert hover["transform"][0]["value"] == "__attaviz_rate_label"


def test_line_resolves_named_date_format():
    data = pd.DataFrame(
        {"date": pd.to_datetime(["2020-01-01", "2021-01-01"]), "value": [1, 2]}
    )

    spec = attaviz.line(data, x="date", y="value", date_format="year").to_dict()

    assert spec["layer"][0]["encoding"]["x"]["axis"]["format"] == "%y"


def test_line_rejects_duplicate_series_keys():
    data = pd.DataFrame({"year": [2020, 2020], "country": ["A", "A"], "value": [1, 2]})

    with pytest.raises(ValueError, match="must be unique"):
        attaviz.line(data, x="year", y="value", series="country")


def test_scatter_highlight_requires_label():
    data = pd.DataFrame({"x": [1, 2], "y": [3, 4]})

    with pytest.raises(ValueError, match="highlight requires label"):
        attaviz.scatter(data, x="x", y="y", highlight="A")


def test_scatter_and_composition_helpers_serialize():
    data = pd.DataFrame({"x": [1, 2, 3], "y": [4, 6, 5], "name": ["A", "B", "C"]})
    chart = attaviz.scatter(data, x="x", y="y", label="name", highlight="A")
    chart = attaviz.add_annotation(chart, x=1, y=4, text="Start")
    chart = attaviz.add_reference_line(chart, value=5, axis="y", label="Target")
    chart = attaviz.add_reference_range(chart, start=1.5, end=2.5, axis="x")

    assert "layer" in chart.to_dict()


def test_scatter_renders_highlighted_points_above_muted_points():
    data = pd.DataFrame({"x": [1, 1], "y": [2, 2], "name": ["highlighted", "other"]})

    spec = attaviz.scatter(
        data, x="x", y="y", label="name", highlight="highlighted"
    ).to_dict()

    assert spec["layer"][1]["transform"][0]["filter"]["oneOf"] == ["highlighted"]
    assert spec["layer"][2]["mark"]["type"] == "text"


def test_composition_helper_rejects_ambiguous_encodings():
    first = attaviz.scatter(pd.DataFrame({"x": [1], "y": [2]}), x="x", y="y")
    second = attaviz.scatter(pd.DataFrame({"a": [1], "b": [2]}), x="a", y="b")

    with pytest.raises(TypeError, match="unambiguous"):
        attaviz.add_annotation(first + second, x=1, y=2, text="Ambiguous")


def test_reference_range_rejects_reversed_values():
    data = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    chart = attaviz.scatter(data, x="x", y="y")

    with pytest.raises(ValueError, match="start must not exceed end"):
        attaviz.add_reference_range(chart, start=5, end=1)


def test_frame_requires_description_and_source_for_url():
    data = pd.DataFrame({"category": ["A"], "value": [1]})
    chart = attaviz.bar(data, category="category", value="value")

    with pytest.raises(ValueError, match="must not be empty"):
        attaviz.frame(chart, description="")
    with pytest.raises(ValueError, match="requires source"):
        attaviz.frame(chart, description="One bar", source_url="https://example.com")

    spec = attaviz.frame(
        chart,
        description="One bar showing a value of one.",
        source="Example",
        source_url="https://example.com",
        note="Illustrative data.",
    ).to_dict()
    assert spec["description"] == "One bar showing a value of one."
    assert len(spec["vconcat"]) == 1
    assert spec["title"]["frame"] == "bounds"
    assert spec["title"]["orient"] == "bottom"
    assert spec["usermeta"]["attaviz"]["source_url"] == "https://example.com"


def test_framed_responsive_bar_keeps_full_width_and_hides_raw_axis_title():
    data = pd.DataFrame({"country": ["Indonesia", "Thailand"], "gdp": [1.37e12, 515e9]})
    chart = attaviz.bar(
        data,
        category="country",
        value="gdp",
        value_format="currency",
        currency="USD",
    )
    spec = attaviz.frame(
        chart,
        description="GDP comparison.",
        source="World Bank",
    ).to_dict()

    assert [view.get("width") for view in spec["vconcat"]] == [600]
    assert spec["vconcat"][0]["layer"][0]["encoding"]["x"]["title"] is None
    assert spec["vconcat"][0]["layer"][0]["encoding"]["y"]["axis"]["grid"] is False
    assert spec["title"]["text"] == ["Source: World Bank"]
