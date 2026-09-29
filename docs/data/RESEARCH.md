# Public data for gallery examples

Research checked against World Bank documentation and live API responses on
2026-09-25 and refreshed for the committed chart snapshots on 2026-09-29.

## Recommendation

Commit small, tidy snapshots under `docs/data/` and keep network calls out of the
Quarto build. The gallery uses separate files shaped for each example so its
code stays focused on chart construction. The Human Capital Index range remains
separate because it belongs to a different World Bank database.

The World Bank Indicators API exposes WDI and more than 45 other databases and
does not require an API key. Its API supports year ranges, pagination, JSON, and
multiple indicator codes in one request ([API overview][api-overview],
[call syntax][api-calls]). Pinning the returned observations makes the examples
short and reproducible while retaining an exact refresh recipe.

## Chart replacements

### Stacked area: Indonesia's employment structure

Use the three modeled ILO employment shares from WDI:

- `SL.AGR.EMPL.ZS` — employment in agriculture (% of total employment)
- `SL.IND.EMPL.ZS` — employment in industry (% of total employment)
- `SL.SRV.EMPL.ZS` — employment in services (% of total employment)

They form a real 100% composition and are a better semantic match for a stacked
area chart than three independently assembled electricity series. A compact
snapshot at 2000, 2005, 2010, 2015, 2020, and 2024 is sufficient for the gallery.
The live [Indonesia API query][employment-query] is the refresh source; the
[agriculture indicator page][employment-metadata] identifies the WDI series,
modeled ILO basis, coverage, and license. Preserve the API's full precision in
the CSV and format or round only in the chart.

### Bubble scatterplot: income, health, and population

Use 2023 observations for Indonesia, Malaysia, the Philippines, Thailand, and
Viet Nam:

- `NY.GDP.PCAP.CD` — GDP per capita (current US$), x position
- `SP.DYN.LE00.IN` — life expectancy at birth, total (years), y position
- `SP.POP.TOTL` — population, total, bubble area

All 15 observations are present in the live [multi-indicator API query][bubble-query].
Indicator definitions and original providers are returned by the official
metadata endpoints for [GDP per capita][gdp-metadata], [life expectancy][life-metadata],
and [population][population-metadata]. Divide population by one million in an
Altair transform or for display only; keep the source value in people.

### Slope chart: access to electricity

Use `EG.ELC.ACCS.ZS`, access to electricity (% of population), for the same five
countries in 2010 and 2023. Both endpoints are present for all five countries in
the [API range query][electricity-query]. Filter the committed snapshot to the
two endpoint years so the gallery code remains about the slope chart, not data
wrangling. The [indicator metadata][electricity-metadata] attributes the series
to the World Bank's SDG 7.1.1 Electrification Dataset.

### Line with uncertainty band: Human Capital Index, with caveat

WDI source 2 has no indicator triplet for a point estimate with lower and upper
bounds. Do not manufacture a WDI confidence interval. The closest honest World
Bank Indicators API example is the Human Capital Index database (source 63):

- `HD.HCI.OVRL` — point estimate
- `HD.HCI.OVRL.LB` — lower bound
- `HD.HCI.OVRL.UB` — upper bound

The [HCI API query][hci-query] returns these series for the five countries and
includes observations for 2017, 2018, and 2020 (with some country-year gaps).
This can demonstrate an uncertainty band, but the title and source must say
**Human Capital Index**, not WDI. The [lower-bound metadata endpoint][hci-metadata]
confirms the separate source. If a continuous annual band is more important
than development subject matter, retain a standard Altair/vega dataset instead;
it is clearer than interpolating sparse HCI bounds.

## Reuse, attribution, and snapshot notes

The WDI catalog record classifies the dataset as public and licenses it under
CC BY 4.0 ([WDI catalog][wdi-catalog]). World Bank dataset terms permit copying,
adapting, distributing, and API use unless metadata says otherwise. They require
attribution to the World Bank and its data providers and warn that some
third-party indicators may have additional terms ([summary terms][terms]).
Therefore, retain each indicator's `sourceOrganization` in this research record
or snapshot metadata and recheck it whenever the files are refreshed.

Suggested source line for WDI snapshots:

> Source: World Bank, World Development Indicators; original data providers
> listed in indicator metadata. CC BY 4.0. Retrieved 2026-09-25. Adapted for
> Attaviz documentation.

For the range example, replace “World Development Indicators” with “Human
Capital Index.” Also record the retrieval date, exact API URL, selected years
and countries, dropped nulls, unit conversions, and any derived fields in
`docs/data/README.md`. Do not call the live API during documentation builds:
WDI observations are revised, so a live build would not be reproducible.

[api-overview]: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
[api-calls]: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
[employment-query]: https://api.worldbank.org/v2/country/IDN/indicator/SL.AGR.EMPL.ZS;SL.IND.EMPL.ZS;SL.SRV.EMPL.ZS?source=2&date=2000:2024&format=json&per_page=1000
[employment-metadata]: https://data.worldbank.org/indicator/SL.AGR.EMPL.ZS
[bubble-query]: https://api.worldbank.org/v2/country/IDN;VNM;PHL;THA;MYS/indicator/NY.GDP.PCAP.CD;SP.DYN.LE00.IN;SP.POP.TOTL?source=2&date=2023&format=json&per_page=1000
[gdp-metadata]: https://api.worldbank.org/v2/indicator/NY.GDP.PCAP.CD?source=2&format=json
[life-metadata]: https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?source=2&format=json
[population-metadata]: https://api.worldbank.org/v2/indicator/SP.POP.TOTL?source=2&format=json
[electricity-query]: https://api.worldbank.org/v2/country/IDN;VNM;PHL;THA;MYS/indicator/EG.ELC.ACCS.ZS?source=2&date=2010:2023&format=json&per_page=1000
[electricity-metadata]: https://api.worldbank.org/v2/indicator/EG.ELC.ACCS.ZS?source=2&format=json
[hci-query]: https://api.worldbank.org/v2/country/IDN;VNM;PHL;THA;MYS/indicator/HD.HCI.OVRL;HD.HCI.OVRL.LB;HD.HCI.OVRL.UB?source=63&format=json&per_page=1000
[hci-metadata]: https://api.worldbank.org/v2/indicator/HD.HCI.OVRL.LB?source=63&format=json
[wdi-catalog]: https://datacatalog.worldbank.org/search/dataset/0037712/world-development-indicators
[terms]: https://data.worldbank.org/summary-terms-of-use
