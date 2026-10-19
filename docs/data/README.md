# Gallery boundary data

`southeast-asia.geojson` contains the eleven Southeast Asian country records
used by the choropleth gallery example. Geometry and 2019 population and GDP
estimates come from Natural Earth 1:50m Admin 0 Countries, version 5.1.1.

Natural Earth data is public domain and represents de facto boundaries. This
subset is documentation data, not a boundary dataset distributed by Attaviz.

Source: <https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries-2/>

## World Development Indicators snapshots

`wdi-southeast-asia-2023.csv` contains 2023 GDP, GDP per capita, life
expectancy, population, and modeled ILO employment shares for seven Southeast
Asian economies. `wdi-electricity-access-2022.csv` contains urban and rural
electricity-access rates for the same economies in 2022.

`wdi-indonesia-employment.csv` contains agriculture, industry, and service
employment shares for Indonesia in 2000, 2005, 2010, 2015, 2020, and 2024.
It drops null observations and reshapes the three indicator series into the
`year`, `sector`, and `share` columns used by the stacked-area example.

`wdi-electricity-access-2010-2023.csv` contains total electricity-access rates
for Cambodia, Indonesia, Lao PDR, Myanmar, and the Philippines in 2010 and
2023. Percent values from the API are divided by 100 for Vega-Lite percent
formatting. Null observations are omitted.

`hci-range.csv` contains Human Capital Index estimates and lower and upper
bounds for the same five countries in 2010, 2017, 2018, and 2020 where all three
values are available. The three source series are reshaped into `estimate`,
`lower`, and `upper` columns; the Philippines has no 2010 observation.

The original two snapshots were retrieved on 2026-09-25. The three chart-type
snapshots were retrieved on 2026-09-29. Values are stored at source precision,
apart from display-oriented rounding in the urban/rural file. They are not
imported by the Attaviz package or refreshed during documentation builds.

Refresh URLs:

- [Indonesia employment](https://api.worldbank.org/v2/country/IDN/indicator/SL.AGR.EMPL.ZS;SL.IND.EMPL.ZS;SL.SRV.EMPL.ZS?source=2&date=2000:2024&format=json&per_page=1000)
- [Electricity access](https://api.worldbank.org/v2/country/IDN;VNM;PHL;THA;MYS/indicator/EG.ELC.ACCS.ZS?source=2&date=2010:2023&format=json&per_page=1000)
- [Human Capital Index range](https://api.worldbank.org/v2/country/IDN;VNM;PHL;THA;MYS/indicator/HD.HCI.OVRL;HD.HCI.OVRL.LB;HD.HCI.OVRL.UB?source=63&format=json&per_page=1000)

Sources: World Bank, World Development Indicators and Human Capital Index.
CC BY 4.0. Original data providers are identified in each indicator's metadata.
See `RESEARCH.md` for API documentation, licensing details, indicator codes,
and refresh URLs.
