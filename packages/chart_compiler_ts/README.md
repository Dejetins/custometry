# Canonical line compiler

`compileLineChart` implements only the MS-003 S03 canonical `line` specification
over `sales-report/v1` daily net revenue. It produces allowlisted ECharts options
and exact decimal-string table rows from the same input. It does not import an
engine, fetch data, aggregate, persist results, authorize access or provide exports.

The consumer must reauthorize the server response, verify the spec/reference
content hashes, and resolve the render colors from the pinned system defaults.
The compiler then checks the closed specification, workspace/owner/policy,
artifact and metric bindings, schema/grain/size and supported formatting. Extra
fields, executable content and remote assets fail closed. Previous-year values
align by calendar date; the full comparison table retains its original dates.
Decimal-to-number conversion is restricted to chart coordinates; table strings
remain exact. The Web adapter still owns SVG rendering, bundled fonts and the
complete render manifest/identity.

The synthetic contract fixture was produced by
`packages.presentation.domain.reports.line_spec` / `versioned` and the registered
`packages.semantic_model.application.sales_metrics.definitions` on 2026-09-13.
It contains no provider rows and proves no database/browser journey.

Validation: `corepack pnpm --filter @custometry/chart-compiler typecheck` and
`corepack pnpm --filter @custometry/chart-compiler test`.
Real API/Web SVG integration and the bounded proof are recorded in the
[S04 report](../../.codex/delivery/evidence/MS-003/MS-003-S04/report.md).
