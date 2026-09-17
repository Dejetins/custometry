# Normalized pilot comparison — MS-003-S04

Source: preserved `docs/architecture/ui/target-pilot/ru/source.html`, SHA-256
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
Both captures use Chromium at 1920x1080 or 768x1024, RU, the overview/chart
surface and the open Trust inspector. The source uses its own customer fixture;
the implementation uses the actual prepared receipt-sales result. Exact data
and supported controls therefore differ by the accepted milestone scope.
The pilot was also inspected before implementation (preserved attempt-1 evidence).

| Comparison | Source | Implementation |
|---|---|---|
| Wide desktop | [Pilot](browser/pilot-1920.png) | [Report](browser/report-1920-ru.png) |
| Narrow desktop | [Pilot](browser/pilot-768.png) | [Report](browser/report-768-ru.png) |
| Complete table / Trust | Source chart/table structure | [Table](browser/table-trust-1920-ru.png) |
| Reflow smoke | Not a source-fidelity state | [200% narrow RU](browser/zoom-768-ru.png) |

Observed retained structure: compact graphite navigation rail, framed document,
context title and tabs, horizontal metric rail, chart header with table/Focus
controls, bordered content panel, docked inspector at wide desktop, cyan actions,
muted secondary typography and clear keyboard focus. Chart and table reuse the
same server daily series. Focus contains both and returns to its trigger.

Scoped differences: three receipt metrics replace the pilot's customer metric
family; a single canonical net-revenue line replaces channel/segment small
multiples. S03's pinned system BrandProfile supplies the purple line. The explicit
editor fields and Apply/Save explanation add vertical height, especially at 768px.
The 768px inspector follows the chart in document order and requires vertical
scroll; the source's much larger inspector is not copied over the report.
Only the overview page exists; its inactive document labels are not false links.
Unsupported segments, comments, publication, exports, arbitrary authoring and
view-management controls are omitted. These are bounded omissions, not a claim
that the complete pilot or all route-blueprint capabilities are implemented.

The 200% test sets the document CSS zoom to 2 in the actual browser and verifies
paint/layout reflow without page-wide horizontal overflow. It is not a native
browser-toolbar zoom or full WCAG certification. Native platform font fallback
is retained; no new downloadable font, complete renderer manifest, pixel-error
threshold or design-system certification is claimed. S06 owns final owner visual
acceptance. Screenshots contain only demo aggregate report values and safe result
identities; no sign-in credentials, cookies, DSNs or provider rows are retained.
