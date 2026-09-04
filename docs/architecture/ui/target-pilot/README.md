# Target UI concept

The product owner selected this final interactive pilot as the target Custometry
UI concept on 2026-09-04. It defines the composition, navigation, panels,
controls, visual treatment, and interactions actually demonstrated by the
pilot. It is more than a color or density reference. Future implementation
must follow these decisions, identify concrete missing states, and resolve
material deviations with the owner rather than substitute later G3/G4 boards.

## Open the concept

From the repository root, run:

```bash
python3 -m http.server 8834 --bind 127.0.0.1 --directory docs/architecture/ui/target-pilot
```

Then open [the pilot](http://127.0.0.1:8834/ru/source.html). The HTML includes
both Russian and English; use the language control inside the report-view
settings. The relative ECharts asset and its license are bundled locally.
No G-program runner, Vite application, external CDN, or design service is
required to serve this concept.

## What to carry into production

- Compact navigation rail with hierarchical contextual navigation, preserving
  the product destinations and workspace context.
- Analytical document tabs, metric rail, report context, and docked inspector.
- Report-level period/comparison/filter/grouping state with explicit block
  inheritance and local overrides.
- Chart/table alternatives, shared table geometry, readable labels, one
  analytical S/M/L setting, and adaptive series controls.
- Shared Focus view retaining chart and full table, URL state, close/Escape,
  and focus restoration.
- Inspector filter builder, result trust, methodology, author and discussion
  surfaces, saved personal views, and snapshot-share preflight.
- Mode-aware PNG/SVG and XLSX/CSV exports and RU/EN behavior.

[Concept notes](concept-notes.json) preserve the chronological owner corrections
and requirement bindings from the pilot's source manifest, including product
and API/persistence work still needed. Some early notes were superseded by
later corrections (for example sidebar and text-size controls); the final HTML
is the source for the shown UI. Do not turn contradictory historical notes into
simultaneous requirements.

The machine product blueprint and human mirror retain business semantics,
permissions, computations, identities, and backend requirements. The
[UI blueprint](../../../../custometry-ui-blueprint-ru.md) retains all-screen
scope, states, and functional requirements, including screens absent from this
pilot. ADR-0007 retains the selected production frontend technology. Fixture
data, demo calculations, browser localStorage, and email/share preflights are
not production backend behavior or authorization. Carry these seams into
bounded implementation work rather than treating the demo as already shipped.

## Identity and preservation

[Manifest](manifest.json) pins the exact HTML, ECharts runtime, and license.
These three files were relocated byte-for-byte from the old
`pilot-candidate-v3-metadata` directory. The HTML SHA-256 is
`b54b8b77d677d57869b0065dbe3aa005f13070297dface19ba98938f50d83700`.
The old name was bookkeeping for a derived pilot with non-rendering QA
metadata; it is not a new required workflow or a version-selection rule.

The owner explicitly replaced the previous restriction to a visual-language
anchor. The earlier August 5 pilot and the later G-stage boards are historical
sources, not competing current UI concepts. Their recovery point is documented
in [UI-program retirement](../ui-program-retirement.md).

## Delivery boundary

Use the [Web implementation source contract](../custometry-web-implementation-source-contract-v1.md)
and ordinary bounded tickets. The current production code remains intact;
conformance to this concept is subsequent implementation work. A route already
marked implemented is not thereby certified as matching this concept.

Keep browser traces, repeated screenshots, generated boards, intermediate
inventories, and local experiment outputs out of the maintained source tree.
Retain compact implementation evidence once at the tested boundary. Do not
restart the retired G0-G6 program to implement this concept.
