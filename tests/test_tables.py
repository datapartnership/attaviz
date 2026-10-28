"""Table rendering, input isolation, and optional dependency behavior."""

import builtins
from html.parser import HTMLParser

import pandas as pd
import pytest

import attaviz


def test_table_renders_and_supports_native_formatting():
    from great_tables import GT

    data = pd.DataFrame(
        {
            "Country": ["Indonesia", "Malaysia"],
            "Count": [12345, 900],
            "Share": [0.125, None],
        }
    )
    original = data.copy(deep=True)
    result = attaviz.table(
        data, title="Example", subtitle="Selected countries", source="Source: example"
    )
    assert isinstance(result, GT)
    html = (
        result.fmt_integer(columns="Count").fmt_percent(columns="Share").as_raw_html()
    )
    for text in [
        "Example",
        "Selected countries",
        "Source: example",
        "12,345",
        "12.50%",
        "N/A",
    ]:
        assert text in html
    assert 'scope="col"' in html
    assert "gt_right" in html
    assert "Open Sans" in html
    assert 'id="title" style="font-weight: 700; padding-bottom: 0;"' in html
    pd.testing.assert_frame_equal(data, original)
    data.loc[0, "Country"] = "Changed"
    assert "Changed" not in result.as_raw_html()


def test_table_escapes_text_and_preserves_unformatted_precision():
    text = "<script>alert(1)</script>"
    result = attaviz.table(
        pd.DataFrame({text: [text], "Value": [0.123456789]}),
        title=text,
        subtitle=text,
        source=text,
    )
    html = result.as_raw_html()
    assert text not in html
    assert html.count("&lt;script&gt;") >= 5
    assert "0.123456789" in html


@pytest.mark.parametrize(
    "data, error, match",
    [
        ([1], TypeError, "pandas DataFrame"),
        (pd.DataFrame(), ValueError, "at least one row"),
        (pd.DataFrame([[1, 2]], columns=["a", "a"]), ValueError, "unique string"),
        (pd.DataFrame({1: [2]}), ValueError, "unique string"),
    ],
)
def test_table_rejects_invalid_data(data, error, match):
    with pytest.raises(error, match=match):
        attaviz.table(data)


def test_table_without_title_and_subtitle_validation():
    data = pd.DataFrame({"Country": ["Indonesia"]})
    assert "Indonesia" in attaviz.table(data).as_raw_html()
    with pytest.raises(ValueError, match="subtitle requires a title"):
        attaviz.table(data, subtitle="Subtitle")


def test_missing_tables_extra_has_install_instructions(monkeypatch):
    original_import = builtins.__import__

    def without_great_tables(name, *args, **kwargs):
        if name == "great_tables":
            raise ImportError("Not installed")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_great_tables)
    with pytest.raises(ImportError, match=r"attaviz\[tables\]"):
        attaviz.table(pd.DataFrame({"value": [1]}))


@pytest.mark.parametrize("subtitle", [None, "Selected countries"])
def test_table_groups_title_and_subtitle_without_removing_outer_spacing(subtitle):
    class HeadingStyles(HTMLParser):
        def __init__(self):
            super().__init__()
            self.cells = {}

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag == "td" and attrs.get("id") in {"title", "subtitle"}:
                self.cells[attrs["id"]] = attrs.get("style", "")

    result = attaviz.table(
        pd.DataFrame({"Country": ["Indonesia"]}), title="Example", subtitle=subtitle
    )
    headings = HeadingStyles()
    headings.feed(result.as_raw_html())
    title = headings.cells["title"]
    assert "padding-top" not in title
    if subtitle is None:
        assert "subtitle" not in headings.cells
        assert "padding-bottom" not in title
    else:
        assert "padding-bottom: 0;" in title
        assert "padding-top: 3px;" in headings.cells["subtitle"]
        assert "padding-bottom" not in headings.cells["subtitle"]


def test_table_preserves_full_labels_with_native_widths_and_row_striping():
    label = "People who completed the program (%)"
    result = (
        attaviz.table(
            pd.DataFrame({"Country": ["Indonesia", "Malaysia"], "Share": [0.876, None]})
        )
        .cols_label(Share=label)
        .cols_width(Country="150px", Share="130px")
        .fmt_percent(columns="Share", decimals=1)
        .opt_row_striping()
    )
    html = result.as_raw_html()
    for text in [
        label,
        "Indonesia",
        "87.6%",
        "N/A",
        "width:150px;",
        "gt_right gt_striped",
    ]:
        assert text in html
    assert 'data-quarto-disable-processing="true"' in html
    assert "white-space: normal; overflow: visible;" in html
    assert f"background-color: {attaviz.GREY_100}" in html
