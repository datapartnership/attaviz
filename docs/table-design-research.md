# Publication table design research

Reviewed: 27 October 2026. Scope: static publication tables produced by
`attaviz.table()`, including their presentation in Quarto. These sources inform
Attaviz defaults; they do not replace WBG typography and color tokens.

## Guidance from primary sources

| Topic | Guidance | Source |
|---|---|---|
| Heading hierarchy | Give the table a title; preferably pair a message headline with a statistical subtitle identifying the measure, geography, and period. | [Government Analysis Function: tables, Titles](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/#titles) |
| Numeric comparison | Right-align numeric columns and their headings; use consistent precision within a column, thousands separators, and leading zeros for fractions. Keep related numbers close together. | [Government Analysis Function: tables](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/#comparing-numbers) |
| Units and order | State units in column headings or the title. Use meaningful category order; rankings can serve comparison, while dates and ordered groups should retain their natural order. | [Government Analysis Function: tables](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/) |
| Rules and shading | Limit gridlines and shading. A rule beneath the column headings and rules around summaries are usually sufficient. Shading must not carry meaning on its own. | [Government Analysis Function: tables](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/#gridlines) |
| Notes and sources | Prefer explanations near the relevant content. If necessary, place footnote markers on headings or labels rather than numbers. Put source information below the table. | [Government Analysis Function: tables](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-tables/#footnotes) |
| Missing values | Explain missing-value notation. The Analysis Function discourages ambiguous NA notation and distinguishes unavailable from inapplicable and confidential data. | [Government Analysis Function: symbols and shorthand](https://analysisfunction.civilservice.gov.uk/policy-store/symbols-in-tables-definitions-and-help/#no-to-na) |
| Accessible naming and headers | Captions help readers find and understand a table. Identify row and column headers structurally, using appropriate `scope`, `id`, and `headers` relationships. | [GOV.UK: Table](https://design-system.service.gov.uk/components/table/), [W3C WAI: Tables tutorial](https://www.w3.org/WAI/tutorials/tables/) |
| Complexity and small screens | Prefer simpler tables and preserve header/data relationships across responsive formats. Horizontal scrolling is one possible approach; reducing text size alone does not address complexity. | [W3C WAI: Table tips](https://www.w3.org/WAI/tutorials/tables/tips/), [ONS: Table component](https://service-manual.ons.gov.uk/design-system/components/table) |
| Heading control | Great Tables exposes heading alignment, title/subtitle font sizes and weights, and heading padding. Its padding option is an implementation mechanism rather than a table-design recommendation. | [Great Tables: `tab_options()`](https://posit-dev.github.io/great-tables/reference/GT.tab_options.html) |

None of these sources specifies a universal title–subtitle gap in pixels.
A smaller inner gap than the separation between the heading group and the data
is an Attaviz design judgment, consistent with treating title and subtitle as
one group.

## What the current helper already provides

Source inspection of `src/attaviz/tables.py` and a generated HTML sample showed:

- Native HTML tables, numeric/text alignment, column-header `scope` and data-cell
  `headers` associations supplied by Great Tables.
- One font family stack, clear title/subtitle hierarchy, tabular numerals, white
  background, and subtle horizontal rules without a vertical grid.
- Explicit formatting through native Great Tables methods, preserving numeric
  precision until the author chooses a display format.
- Plain-text titles, subtitles, and source notes, with source notes below data.

These are implementation observations, not a claim of full accessibility
conformance or independent usability testing.

## Recommendations for Attaviz

1. **Tighten the title–subtitle gap.** Before the spacing fix, the installed
   renderer emitted 9 px title bottom padding and 8 px subtitle top padding:
   17 px between adjacent heading cells, before line-box whitespace. Reduce
   their adjoining padding while preserving the outer heading spacing. Reuse
   the existing spacing tokens and check long, wrapped headings visually.
2. **Keep light rules as the default.** Avoid adding stripes or a full cell grid
   automatically. This is a restrained Attaviz choice, not a claim that every
   table must avoid striping.
3. **Document author responsibilities.** Choose meaningful order, units, and
   precision; explain `N/A` explicitly. The helper cannot infer why data is
   missing, so keep the existing default for compatibility and allow native
   `.sub_missing()` customization when a publication needs another notation.
4. **Prefer semantic HTML for web publication.** PNG is useful for slides but
   does not preserve the table's structural relationships; exporting an image
   or PDF does not itself demonstrate accessibility. See [W3C WAI's structural
   requirements](https://www.w3.org/WAI/tutorials/tables/).
5. **Audit multi-table pages separately.** The inspected Great Tables version
   emits repeated `id="title"`, `id="subtitle"`, and column IDs across tables,
   referenced by ARIA/`headers`. Unique wrapper IDs do not resolve this alone.
   Check assistive-technology behavior and upstream support before claiming
   that multiple embedded tables have reliable accessible naming.
6. **Check narrow and zoomed layouts.** A 100% table width alone does not prove
   that long labels, large values, spanners, and footnotes fit. Verify overflow
   in both standalone exports and Quarto, preserving data/header associations.

This research did not include user testing, a screen-reader audit, or an
assessment of exported PDF tagging. No new table features are proposed by the
spacing fix.

## UX/UI perspective: practitioner patterns and design systems

[Pencil & Paper's table-pattern analysis](https://www.pencilandpaper.io/articles/ux-pattern-analysis-enterprise-data-tables)
is useful as an illustrated checklist for alignment, density, separators, and
richer cells. It is practitioner pattern synthesis, not a controlled study
establishing universal rules. Treat its absolute alignment advice and example
pixel sizes as contextual heuristics.

[NN/g's four major table tasks](https://www.nngroup.com/articles/data-tables/)
provides a complementary framework: find records, compare values, inspect/edit
records, and act on records. It includes observations and an eye-tracking
example. Attaviz's static tables primarily serve finding and comparison;
editing, filtering controls, and bulk actions are not implied additions.

[IBM Carbon's data-table guidelines](https://www.carbondesignsystem.com/building-blocks/core/components/data-table/guidelines)
provide implemented product conventions for titles, descriptions, concise
headers, density choices, and optional zebra stripes. These are system-specific
choices rather than empirical proof of an optimal publication-table style.
The separate [Carbon v10 style page](https://v10.carbondesignsystem.com/components/data-table/style/)
is historical, not the current specification.

### What applies to Attaviz

| Detail | Application and limits |
|---|---|
| Width and adjacency | NN/g recommends a readable identifier first and related columns together. Our application: size columns for actual content; avoid large gaps between measures being compared. |
| Alignment | Pencil & Paper recommends text left, quantities right, and matching header alignment. Dates and numeric identifiers need semantic judgment. Its “never center” heuristic need not forbid centered status symbols. Attaviz's existing tabular numerals preserve aligned digits without switching WBG's font to monospace. |
| Header wrapping | Carbon recommends concise labels, then limited wrapping/truncation with a tooltip. Our static/export adaptation: prefer complete wrapped labels or shorter wording retaining units; hover disclosure may not survive export. |
| Density | Carbon and Pencil & Paper illustrate different size scales. Choose padding for the actual reading task and allow wrapped text; their UI row heights are not universal Attaviz requirements. |
| Rules and stripes | Pencil & Paper warns about stripes competing with selection/hover states; Carbon and NN/g allow stripes to aid row tracking. Keep light rules as a restrained default, but test subtle stripes for wider tables rather than banning them. |
| In-cell visuals | Pencil & Paper illustrates icons and bars. Our application: add only task-relevant encodings, retaining exact values, deliberate scales, and explanations beyond color. |

[NN/g's visual-indicator study](https://www.nngroup.com/articles/visual-indicators-differentiators/)
tested 96 participants on four mobile pages, including stock tables. Combining
icon and color improved locating marked items compared with text alone. This
supports meaningful indicators for that task, not decorative icons everywhere.

[Ji, Périn, and Nacenta's controlled table-reading study](https://ieeevis.b-cdn.net/vis_2024/pdfs/v-full-1288.pdf)
adds task-specific evidence: color and bars helped find maxima, while zebra
striping helped more with proportional-difference comparisons. Its static
conditions are relevant to publication tables, but do not establish a universal
winner or an optimal title gap.

These sources complement statistical guidance and W3C semantics. They identify
alternatives to test with readers; they do not justify copying enterprise-grid
features or changing UI automatically. No UI or code changes are part of this
research addition.

## Implemented defaults

Attaviz now uses content-based table width with automatic column layout, 6 px
vertical and 9 px horizontal cell padding, and wrapping headers/body text.
Body text aligns to the top when rows wrap; numeric alignment and tabular
figures remain native to the existing theme. The 3 px internal heading gap
is preserved. Quarto postprocessing is disabled so host table classes do not
replace these choices.

Light horizontal rules remain the default. Native `opt_row_striping()` uses the
WBG light-grey token, with guide/gallery examples removing internal rules for
striped tables. Authors can use native `cols_width()` and `tab_options()` for
width and density rather than new Attaviz arguments. No new interactive table
features were added.
