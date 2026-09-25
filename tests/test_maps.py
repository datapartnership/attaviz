import geopandas as gpd
import pytest
from geopandas.testing import assert_geodataframe_equal
from shapely.geometry import Point, box

import attaviz


def geodata():
    return gpd.GeoDataFrame(
        {"region": ["West", "East", "North"], "rate": [-0.2, 0.4, None]},
        geometry=[box(0, 0, 1, 1), box(1, 0, 2, 1), box(0, 1, 1, 2)],
        crs="EPSG:4326",
    )


def test_choropleth_serializes_missing_highlight_and_does_not_mutate():
    data = geodata()
    original = data.copy()

    chart = attaviz.choropleth(
        data,
        value="rate",
        label="region",
        meaning="change",
        highlight="East",
        title="Change",
    )
    spec = chart.to_dict()

    assert spec["width"] == 600
    assert spec["height"] == 400
    assert spec["projection"]["type"] == "equalEarth"
    assert spec["layer"][0]["mark"]["fill"] == attaviz.NO_DATA
    assert spec["layer"][1]["encoding"]["color"]["scale"]["domain"] == [-0.4, 0.4]
    assert (
        spec["layer"][2]["encoding"]["stroke"]["condition"]["value"]
        == attaviz.SELECTION_PRIMARY
    )
    assert_geodataframe_equal(data, original)


@pytest.mark.parametrize(
    ("classification", "kwargs", "scale_type", "range_size"),
    [
        ("equal_interval", {"classes": 2}, "quantize", 2),
        ("quantile", {"classes": 2}, "quantile", 2),
        ("custom", {"breaks": [0]}, "threshold", 2),
    ],
)
def test_choropleth_classifications(classification, kwargs, scale_type, range_size):
    spec = attaviz.choropleth(
        geodata(),
        value="rate",
        label="region",
        meaning="change",
        classification=classification,
        **kwargs,
    ).to_dict()
    scale = spec["layer"][1]["encoding"]["color"]["scale"]
    assert scale["type"] == scale_type
    assert len(scale["range"]) == range_size


def test_choropleth_rejects_unsafe_geodata():
    data = geodata().set_crs(None, allow_override=True)
    with pytest.raises(ValueError, match="known CRS"):
        attaviz.choropleth(data, value="rate", label="region")

    points = gpd.GeoDataFrame(
        {"region": ["A"], "rate": [1]}, geometry=[Point(0, 0)], crs="EPSG:4326"
    )
    with pytest.raises(ValueError, match="invalid polygon geometry"):
        attaviz.choropleth(points, value="rate", label="region")


def test_map_annotation_serializes_repeatedly_and_warns_outside_bounds():
    chart = attaviz.choropleth(
        geodata(), value="rate", label="region", meaning="change"
    )
    chart = attaviz.add_map_annotation(
        chart, longitude=0.5, latitude=0.5, text="West", position="above"
    )
    chart = attaviz.add_map_annotation(
        chart, longitude=1.5, latitude=0.5, text="East", position="right", marker=False
    )
    spec = chart.to_dict()
    assert spec["projection"]["type"] == "equalEarth"
    assert len(spec["layer"]) == 5

    framed = attaviz.frame(chart, description="An annotated map.").to_dict()
    assert framed["usermeta"]["attaviz"]["map_bounds"] == [0.0, 0.0, 2.0, 2.0]
    assert "usermeta" not in framed["vconcat"][0]

    with pytest.warns(UserWarning, match="outside"):
        attaviz.add_map_annotation(chart, longitude=10, latitude=10, text="Outside")


def test_map_currency_requires_code():
    with pytest.raises(ValueError, match="currency is required"):
        attaviz.choropleth(
            geodata(),
            value="rate",
            label="region",
            meaning="change",
            value_format="currency",
        )


def test_map_currency_formats_legend():
    spec = attaviz.choropleth(
        geodata(),
        value="rate",
        label="region",
        meaning="change",
        classification="custom",
        breaks=[0],
        value_format="currency",
        currency="USD",
    ).to_dict()

    legend = spec["layer"][1]["encoding"]["color"]["legend"]
    assert "USD" in legend["labelExpr"]
    assert legend["values"] == [0.0]
    assert legend["type"] == "symbol"
