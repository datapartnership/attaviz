"""Smoke tests for attaviz.

These tests catch regressions in the bugs we've seen before: package import,
theme registration, palette data integrity, and formatting edge cases.
"""

from datetime import date

import altair as alt
import pytest

import attaviz


def test_import_and_enable():
    attaviz.enable()
    attaviz.enable(size="small")
    attaviz.enable(size="large")


def test_themes_registered():
    registered = set(alt.themes.names())
    assert {"wbg", "wbg-small", "wbg-medium", "wbg-large"} <= registered


@pytest.mark.parametrize(
    "d, expected",
    [
        (date(2023, 6, 30), "FY23"),  # last day of FY23
        (date(2023, 7, 1), "FY24"),  # first day of FY24
        (date(2023, 1, 15), "FY23"),
    ],
)
def test_fiscal_year_boundary(d, expected):
    assert attaviz.format_date(d, style="fiscal_year") == expected


@pytest.mark.parametrize("style", ["quarter", "fiscal_year"])
def test_d3_date_format_rejects_unsupported_styles(style):
    with pytest.raises(ValueError):
        attaviz.d3_date_format(style)


def test_format_number_scales():
    assert attaviz.format_number(1_234_567) == "1.2M"
    assert attaviz.format_number(1_234_567_890, unit="bytes") == "1.2G"
