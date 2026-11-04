# Restored result download controls

Owner requested restoration of the existing chart/table save/download functionality. The preserved pilot contains mode-aware PNG/SVG and XLSX/CSV menus. Its CSV, inline-string worksheet and stored-ZIP XLSX serializer were adapted into `result-export.ts`; the current production bridge had replaced download/table handlers with unavailable stubs. The configured workspace omitted the old menu entirely.

ResultExportMenu is now present beside expand/collapse in both normal and focus result surfaces. Chart mode offers SVG and PNG 2x; table mode offers CSV and XLSX. Chart export serializes the active ECharts instance with its legend and comparison markup, adding the current surface background. PNG follows the pilot SVG-to-canvas path. Table export reads active table rows, uses unrounded data-value attributes, preserves long decimal strings, and retains null values as blank cells. CSV escaping handles quoted multiline values and formula-prefixed strings; XLSX stores strings as inline strings. No dependency was installed.

Downloads require the server-returned actor permission `report.export_xlsx`, a current applied context and no pending/error results. The asynchronous image path rechecks component presence and enabled state before downloading. This is local export of the currently loaded result; it does not implement a separate backend export-job/preflight/audit pipeline. Report Save remains unchanged. No upload/import capability was inferred from the legacy download menu.

## Verification

Frontend build/TypeScript passed. Frontend suite: 24 files, 116 tests passed, including CSV formula/quoting/high-precision cases. Local grouped gate and whitespace check passed. Browser downloaded all four actual files: SVG and PNG from focus mode, CSV and XLSX from normal table mode. Python verified valid SVG XML, PNG signature and 2x dimensions (2752x1766), ZIP checksums and all XLSX XML members, 31 daily data rows, and identical first raw value 1422.4 in CSV and worksheet B2. PNG and [menu screenshot](restored-export-menu.png) were visually inspected. Final background/revocation changes were followed by repeating all four browser downloads.

One initial browser selector matched both normal and focus export buttons. The corrected test scoped the active focus surface and passed. No reports were saved or fixtures modified. Synthetic local data only. No publication or production authorization proof is claimed. This is an owner-authorized bounded follow-up to [W40](../../tickets/W40-WORKSET-CATALOGUE-INTERACTIONS.md).

## Owner follow-up: minimal export controls

Removed the extension suffix from the Excel label. Export options now have no resting background or border and use a subtle hover highlight. The download trigger shares the transparent expand/collapse control styling in both normal and focus surfaces. Native buttons and keyboard focus outlines remain intact. Changes are limited to `ResultExportMenu.tsx` and `workspace.css`; serialization and download behavior are unchanged.

Frontend build passed. Browser check at 1480×969 confirmed Excel label, zero-width item borders, transparent resting backgrounds and trigger borders, visible hover feedback, Escape dismissal and focus return. The [updated menu screenshot](export-menu-polish.png) was visually inspected. Local grouped gate and whitespace check passed. Download serialization was not retested for this cosmetic-only follow-up.
