<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="ui-design-program-sha256" content="d1794c20ccf0a5a90b0e3c1863e4169276ac477ca1ca9a79926800f88b07a6bc">
  <title>Custometry Next-Generation Product-wide Web UI Program — screen atlas</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background:#0e1116; color:#eef1f5; }
    * { box-sizing:border-box; } body { margin:0; } main { max-width:1600px; margin:auto; padding:24px; }
    header.hero { display:flex; gap:24px; align-items:flex-end; justify-content:space-between; margin-bottom:32px; }
    h1,h2,h3,p { margin-top:0; } h1 { margin-bottom:8px; font-size:26px; } h2 { font-size:18px; } h3 { margin:14px 0; font-size:15px; }
    .meta,.quiet,.label,dt { color:#929aa6; font-size:12px; } .stats { display:flex; flex-wrap:wrap; gap:8px; }
    .stat,.screen-card,.table-wrap { border:1px solid #2a3039; border-radius:10px; background:#151a21; }
    .stat { min-width:112px; padding:12px; } .stat strong { display:block; font-size:20px; }
    section { margin-top:32px; } .section-head { display:flex; justify-content:space-between; gap:16px; align-items:baseline; }
    .screen-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr)); gap:14px; }
    .screen-card { min-width:0; padding:16px; } .screen-card.blocked { border-color:#7e5421; }
    .screen-head { display:flex; gap:8px; justify-content:space-between; align-items:center; } code { overflow-wrap:anywhere; color:#d8cbff; }
    .representative,.chip { display:inline-flex; align-items:center; min-height:22px; border-radius:5px; background:#242b35; padding:3px 7px; font-size:11px; }
    .representative { background:#3b2b6f; color:#e1d8ff; } .chips { display:flex; flex-wrap:wrap; gap:5px; margin:5px 0 12px; }
    dl { display:grid; gap:6px; } dl div { display:grid; grid-template-columns:72px minmax(0,1fr); gap:8px; } dt,dd { margin:0; overflow-wrap:anywhere; }
    .table-wrap { overflow:auto; } table { width:100%; min-width:720px; border-collapse:collapse; } th,td { padding:10px 12px; border-bottom:1px solid #252b34; text-align:start; vertical-align:top; }
    th { color:#aab2bd; font-size:12px; }
    @media (max-width:760px) { main { padding:16px; } header.hero { align-items:flex-start; flex-direction:column; } }
  </style>
</head>
<body>
<main>
  <header class="hero">
    <div><h1>Custometry Next-Generation Product-wide Web UI Program</h1><p class="meta">Derived screen atlas · revision 4</p></div>
    <div class="stats">
      <div class="stat"><strong>175</strong><span class="meta">screens</span></div>
      <div class="stat"><strong>27</strong><span class="meta">families</span></div>
      <div class="stat"><strong>9</strong><span class="meta">journeys</span></div>
      <div class="stat"><strong>0</strong><span class="meta">blocked</span></div>
    </div>
  </header>
  <p><strong>Responsive web:</strong> required · <strong>Mobile scope:</strong> unauthorized. This atlas is generated evidence, not a source of truth.</p>
  <section><div class="section-head"><h2>Inventory</h2></div><div class="table-wrap"><table><thead><tr><th>Classification</th><th>Count</th></tr></thead><tbody><tr><td>historical_exclusion</td><td>2</td></tr><tr><td>internal_or_non_visual</td><td>22</td></tr><tr><td>overlay</td><td>24</td></tr><tr><td>persistent_shell</td><td>4</td></tr><tr><td>route_backed_transient</td><td>1</td></tr><tr><td>route_flow</td><td>5</td></tr><tr><td>route_screen</td><td>112</td></tr><tr><td>system_state_family</td><td>5</td></tr></tbody></table></div></section>
  <section><div class="section-head"><h2>Journey map</h2></div><div class="table-wrap"><table><thead><tr><th>Journey</th><th>Entry</th><th>Intermediate</th><th>Alternate</th><th>Failure</th><th>Recovery</th><th>Terminal</th><th>External</th><th>Transitions</th></tr></thead><tbody><tr><td><code>data-to-trusted-result</code></td><td><span class="chip">UI-DATA-001</span></td><td><span class="chip">UI-DQ-001</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-AN-012</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-DATA-001 → UI-DQ-001 (forward)</span><span class="chip">UI-DQ-001 → UI-AN-012 (terminal)</span></td></tr><tr><td><code>compose-large-workbook</code></td><td><span class="chip">UI-RPT-001</span></td><td><span class="chip">UI-RPT-002</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-RPT-003</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-RPT-001 → UI-RPT-002 (forward)</span><span class="chip">UI-RPT-002 → UI-RPT-003 (terminal)</span></td></tr><tr><td><code>publish-review-collaborate</code></td><td><span class="chip">UI-AN-013</span></td><td><span class="chip">UI-AN-014</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-OVR-024</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-AN-013 → UI-AN-014 (forward)</span><span class="chip">UI-AN-014 → UI-OVR-024 (terminal)</span></td></tr><tr><td><code>refresh-with-stable-anchors</code></td><td><span class="chip">UI-DASH-001</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-DASH-002</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-DASH-001 → UI-DASH-002 (terminal)</span></td></tr><tr><td><code>define-recalculate-reuse-segment</code></td><td><span class="chip">UI-SEG-001</span></td><td><span class="chip">UI-SEG-002</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-SEG-003</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-SEG-001 → UI-SEG-002 (forward)</span><span class="chip">UI-SEG-002 → UI-SEG-003 (terminal)</span></td></tr><tr><td><code>digital-to-offline-unit-economics</code></td><td><span class="chip">UI-AN-009</span></td><td><span class="chip">UI-PROMO-001</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-PROMO-003</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-AN-009 → UI-PROMO-001 (forward)</span><span class="chip">UI-PROMO-001 → UI-PROMO-003 (terminal)</span></td></tr><tr><td><code>product-category-assortment-inventory</code></td><td><span class="chip">UI-AN-015</span></td><td><span class="chip">UI-DATA-004</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-DATA-005</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-AN-015 → UI-DATA-004 (forward)</span><span class="chip">UI-DATA-004 → UI-DATA-005 (terminal)</span></td></tr><tr><td><code>open-100x30-document-without-duplicate-compute</code></td><td><span class="chip">UI-RPT-001</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-RPT-002</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-RPT-001 → UI-RPT-002 (terminal)</span></td></tr><tr><td><code>adoption-and-performance-operations</code></td><td><span class="chip">UI-ADMIN-005</span></td><td><span class="chip">UI-ADMIN-006</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-OPS-004</span></td><td><span class="quiet">—</span></td><td><span class="chip">UI-ADMIN-005 → UI-ADMIN-006 (forward)</span><span class="chip">UI-ADMIN-006 → UI-OPS-004 (terminal)</span></td></tr></tbody></table></div></section>
  <section><div class="section-head"><h2>Coverage matrix</h2></div><div class="table-wrap"><table><thead><tr><th>Profile</th><th>States</th><th>Roles</th><th>Locales</th><th>Themes</th><th>Viewports</th><th>Cases/screen</th></tr></thead><tbody><tr><td><code>coverage.ui-auth-001</code></td><td><span class="chip">UI-AUTH-001.initial</span><span class="chip">UI-AUTH-001.first_loading</span><span class="chip">UI-AUTH-001.ready</span><span class="chip">UI-AUTH-001.validation_error</span><span class="chip">UI-AUTH-001.failed</span><span class="chip">UI-AUTH-001.session_expired</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-auth-002</code></td><td><span class="chip">UI-AUTH-002.initial</span><span class="chip">UI-AUTH-002.loading</span><span class="chip">UI-AUTH-002.populated</span><span class="chip">UI-AUTH-002.error</span><span class="chip">UI-AUTH-002.permission_denied</span><span class="chip">UI-AUTH-002.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-auth-003</code></td><td><span class="chip">UI-AUTH-003.initial</span><span class="chip">UI-AUTH-003.loading</span><span class="chip">UI-AUTH-003.populated</span><span class="chip">UI-AUTH-003.error</span><span class="chip">UI-AUTH-003.permission_denied</span><span class="chip">UI-AUTH-003.recovery</span></td><td><span class="chip">invited</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-auth-004</code></td><td><span class="chip">UI-AUTH-004.initial</span><span class="chip">UI-AUTH-004.first_loading</span><span class="chip">UI-AUTH-004.ready</span><span class="chip">UI-AUTH-004.validation_error</span><span class="chip">UI-AUTH-004.failed</span><span class="chip">UI-AUTH-004.session_expired</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-auth-005</code></td><td><span class="chip">UI-AUTH-005.initial</span><span class="chip">UI-AUTH-005.loading</span><span class="chip">UI-AUTH-005.populated</span><span class="chip">UI-AUTH-005.error</span><span class="chip">UI-AUTH-005.permission_denied</span><span class="chip">UI-AUTH-005.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-auth-006</code></td><td><span class="chip">UI-AUTH-006.initial</span><span class="chip">UI-AUTH-006.loading</span><span class="chip">UI-AUTH-006.populated</span><span class="chip">UI-AUTH-006.error</span><span class="chip">UI-AUTH-006.permission_denied</span><span class="chip">UI-AUTH-006.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-core-001</code></td><td><span class="chip">UI-CORE-001.initial</span><span class="chip">UI-CORE-001.loading</span><span class="chip">UI-CORE-001.populated</span><span class="chip">UI-CORE-001.error</span><span class="chip">UI-CORE-001.permission_denied</span><span class="chip">UI-CORE-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-001</code></td><td><span class="chip">UI-DATA-001.initial</span><span class="chip">UI-DATA-001.loading</span><span class="chip">UI-DATA-001.populated</span><span class="chip">UI-DATA-001.error</span><span class="chip">UI-DATA-001.permission_denied</span><span class="chip">UI-DATA-001.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-002</code></td><td><span class="chip">UI-DATA-002.initial</span><span class="chip">UI-DATA-002.loading</span><span class="chip">UI-DATA-002.populated</span><span class="chip">UI-DATA-002.error</span><span class="chip">UI-DATA-002.permission_denied</span><span class="chip">UI-DATA-002.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-003</code></td><td><span class="chip">UI-DATA-003.initial</span><span class="chip">UI-DATA-003.loading</span><span class="chip">UI-DATA-003.populated</span><span class="chip">UI-DATA-003.error</span><span class="chip">UI-DATA-003.permission_denied</span><span class="chip">UI-DATA-003.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-004</code></td><td><span class="chip">UI-DATA-004.initial</span><span class="chip">UI-DATA-004.loading</span><span class="chip">UI-DATA-004.populated</span><span class="chip">UI-DATA-004.error</span><span class="chip">UI-DATA-004.permission_denied</span><span class="chip">UI-DATA-004.recovery</span></td><td><span class="chip">WA</span><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-005</code></td><td><span class="chip">UI-DATA-005.initial</span><span class="chip">UI-DATA-005.loading</span><span class="chip">UI-DATA-005.populated</span><span class="chip">UI-DATA-005.error</span><span class="chip">UI-DATA-005.permission_denied</span><span class="chip">UI-DATA-005.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-006</code></td><td><span class="chip">UI-DATA-006.initial</span><span class="chip">UI-DATA-006.loading</span><span class="chip">UI-DATA-006.populated</span><span class="chip">UI-DATA-006.error</span><span class="chip">UI-DATA-006.permission_denied</span><span class="chip">UI-DATA-006.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-007</code></td><td><span class="chip">UI-DATA-007.initial</span><span class="chip">UI-DATA-007.loading</span><span class="chip">UI-DATA-007.populated</span><span class="chip">UI-DATA-007.error</span><span class="chip">UI-DATA-007.permission_denied</span><span class="chip">UI-DATA-007.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-008</code></td><td><span class="chip">UI-DATA-008.initial</span><span class="chip">UI-DATA-008.loading</span><span class="chip">UI-DATA-008.populated</span><span class="chip">UI-DATA-008.error</span><span class="chip">UI-DATA-008.permission_denied</span><span class="chip">UI-DATA-008.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-009</code></td><td><span class="chip">UI-DATA-009.initial</span><span class="chip">UI-DATA-009.loading</span><span class="chip">UI-DATA-009.populated</span><span class="chip">UI-DATA-009.error</span><span class="chip">UI-DATA-009.permission_denied</span><span class="chip">UI-DATA-009.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-010</code></td><td><span class="chip">UI-DATA-010.initial</span><span class="chip">UI-DATA-010.loading</span><span class="chip">UI-DATA-010.populated</span><span class="chip">UI-DATA-010.error</span><span class="chip">UI-DATA-010.permission_denied</span><span class="chip">UI-DATA-010.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-011</code></td><td><span class="chip">UI-DATA-011.initial</span><span class="chip">UI-DATA-011.loading</span><span class="chip">UI-DATA-011.populated</span><span class="chip">UI-DATA-011.error</span><span class="chip">UI-DATA-011.permission_denied</span><span class="chip">UI-DATA-011.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-012</code></td><td><span class="chip">UI-DATA-012.initial</span><span class="chip">UI-DATA-012.loading</span><span class="chip">UI-DATA-012.populated</span><span class="chip">UI-DATA-012.error</span><span class="chip">UI-DATA-012.permission_denied</span><span class="chip">UI-DATA-012.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-013</code></td><td><span class="chip">UI-DATA-013.initial</span><span class="chip">UI-DATA-013.loading</span><span class="chip">UI-DATA-013.populated</span><span class="chip">UI-DATA-013.error</span><span class="chip">UI-DATA-013.permission_denied</span><span class="chip">UI-DATA-013.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-014</code></td><td><span class="chip">UI-DATA-014.initial</span><span class="chip">UI-DATA-014.loading</span><span class="chip">UI-DATA-014.populated</span><span class="chip">UI-DATA-014.error</span><span class="chip">UI-DATA-014.permission_denied</span><span class="chip">UI-DATA-014.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-015</code></td><td><span class="chip">UI-DATA-015.initial</span><span class="chip">UI-DATA-015.loading</span><span class="chip">UI-DATA-015.populated</span><span class="chip">UI-DATA-015.error</span><span class="chip">UI-DATA-015.permission_denied</span><span class="chip">UI-DATA-015.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-016</code></td><td><span class="chip">UI-DATA-016.initial</span><span class="chip">UI-DATA-016.loading</span><span class="chip">UI-DATA-016.populated</span><span class="chip">UI-DATA-016.error</span><span class="chip">UI-DATA-016.permission_denied</span><span class="chip">UI-DATA-016.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-017</code></td><td><span class="chip">UI-DATA-017.initial</span><span class="chip">UI-DATA-017.loading</span><span class="chip">UI-DATA-017.populated</span><span class="chip">UI-DATA-017.error</span><span class="chip">UI-DATA-017.permission_denied</span><span class="chip">UI-DATA-017.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-018</code></td><td><span class="chip">UI-DATA-018.initial</span><span class="chip">UI-DATA-018.loading</span><span class="chip">UI-DATA-018.populated</span><span class="chip">UI-DATA-018.error</span><span class="chip">UI-DATA-018.permission_denied</span><span class="chip">UI-DATA-018.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-019</code></td><td><span class="chip">UI-DATA-019.initial</span><span class="chip">UI-DATA-019.loading</span><span class="chip">UI-DATA-019.populated</span><span class="chip">UI-DATA-019.error</span><span class="chip">UI-DATA-019.permission_denied</span><span class="chip">UI-DATA-019.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>48</td></tr><tr><td><code>coverage.ui-data-020</code></td><td><span class="chip">UI-DATA-020.initial</span><span class="chip">UI-DATA-020.loading</span><span class="chip">UI-DATA-020.populated</span><span class="chip">UI-DATA-020.error</span><span class="chip">UI-DATA-020.permission_denied</span><span class="chip">UI-DATA-020.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-021</code></td><td><span class="chip">UI-DATA-021.initial</span><span class="chip">UI-DATA-021.loading</span><span class="chip">UI-DATA-021.populated</span><span class="chip">UI-DATA-021.error</span><span class="chip">UI-DATA-021.permission_denied</span><span class="chip">UI-DATA-021.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-022</code></td><td><span class="chip">UI-DATA-022.initial</span><span class="chip">UI-DATA-022.loading</span><span class="chip">UI-DATA-022.populated</span><span class="chip">UI-DATA-022.error</span><span class="chip">UI-DATA-022.permission_denied</span><span class="chip">UI-DATA-022.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-023</code></td><td><span class="chip">UI-DATA-023.initial</span><span class="chip">UI-DATA-023.loading</span><span class="chip">UI-DATA-023.populated</span><span class="chip">UI-DATA-023.error</span><span class="chip">UI-DATA-023.permission_denied</span><span class="chip">UI-DATA-023.recovery</span></td><td><span class="chip">WA</span><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-024</code></td><td><span class="chip">UI-DATA-024.initial</span><span class="chip">UI-DATA-024.loading</span><span class="chip">UI-DATA-024.populated</span><span class="chip">UI-DATA-024.error</span><span class="chip">UI-DATA-024.permission_denied</span><span class="chip">UI-DATA-024.recovery</span></td><td><span class="chip">WA</span><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-data-025</code></td><td><span class="chip">UI-DATA-025.initial</span><span class="chip">UI-DATA-025.loading</span><span class="chip">UI-DATA-025.populated</span><span class="chip">UI-DATA-025.error</span><span class="chip">UI-DATA-025.permission_denied</span><span class="chip">UI-DATA-025.recovery</span></td><td><span class="chip">WA</span><span class="chip">DS</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-026</code></td><td><span class="chip">UI-DATA-026.initial</span><span class="chip">UI-DATA-026.loading</span><span class="chip">UI-DATA-026.populated</span><span class="chip">UI-DATA-026.error</span><span class="chip">UI-DATA-026.permission_denied</span><span class="chip">UI-DATA-026.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-data-027</code></td><td><span class="chip">UI-DATA-027.initial</span><span class="chip">UI-DATA-027.loading</span><span class="chip">UI-DATA-027.populated</span><span class="chip">UI-DATA-027.error</span><span class="chip">UI-DATA-027.permission_denied</span><span class="chip">UI-DATA-027.recovery</span></td><td><span class="chip">WA</span><span class="chip">DS</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-028</code></td><td><span class="chip">UI-DATA-028.initial</span><span class="chip">UI-DATA-028.loading</span><span class="chip">UI-DATA-028.populated</span><span class="chip">UI-DATA-028.error</span><span class="chip">UI-DATA-028.permission_denied</span><span class="chip">UI-DATA-028.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-029</code></td><td><span class="chip">UI-DATA-029.initial</span><span class="chip">UI-DATA-029.loading</span><span class="chip">UI-DATA-029.populated</span><span class="chip">UI-DATA-029.error</span><span class="chip">UI-DATA-029.permission_denied</span><span class="chip">UI-DATA-029.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-030</code></td><td><span class="chip">UI-DATA-030.initial</span><span class="chip">UI-DATA-030.loading</span><span class="chip">UI-DATA-030.populated</span><span class="chip">UI-DATA-030.error</span><span class="chip">UI-DATA-030.permission_denied</span><span class="chip">UI-DATA-030.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-data-031</code></td><td><span class="chip">UI-DATA-031.initial</span><span class="chip">UI-DATA-031.loading</span><span class="chip">UI-DATA-031.populated</span><span class="chip">UI-DATA-031.error</span><span class="chip">UI-DATA-031.permission_denied</span><span class="chip">UI-DATA-031.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-dq-001</code></td><td><span class="chip">UI-DQ-001.initial</span><span class="chip">UI-DQ-001.loading</span><span class="chip">UI-DQ-001.populated</span><span class="chip">UI-DQ-001.error</span><span class="chip">UI-DQ-001.permission_denied</span><span class="chip">UI-DQ-001.recovery</span></td><td><span class="chip">DS</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-dq-002</code></td><td><span class="chip">UI-DQ-002.initial</span><span class="chip">UI-DQ-002.loading</span><span class="chip">UI-DQ-002.populated</span><span class="chip">UI-DQ-002.error</span><span class="chip">UI-DQ-002.permission_denied</span><span class="chip">UI-DQ-002.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-dq-003</code></td><td><span class="chip">UI-DQ-003.initial</span><span class="chip">UI-DQ-003.loading</span><span class="chip">UI-DQ-003.populated</span><span class="chip">UI-DQ-003.error</span><span class="chip">UI-DQ-003.permission_denied</span><span class="chip">UI-DQ-003.recovery</span></td><td><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-dq-004</code></td><td><span class="chip">UI-DQ-004.initial</span><span class="chip">UI-DQ-004.loading</span><span class="chip">UI-DQ-004.populated</span><span class="chip">UI-DQ-004.error</span><span class="chip">UI-DQ-004.permission_denied</span><span class="chip">UI-DQ-004.recovery</span></td><td><span class="chip">DS</span><span class="chip">AN</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-dq-005</code></td><td><span class="chip">UI-DQ-005.initial</span><span class="chip">UI-DQ-005.loading</span><span class="chip">UI-DQ-005.populated</span><span class="chip">UI-DQ-005.error</span><span class="chip">UI-DQ-005.permission_denied</span><span class="chip">UI-DQ-005.recovery</span></td><td><span class="chip">DS</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-001</code></td><td><span class="chip">UI-AN-001.initial</span><span class="chip">UI-AN-001.loading</span><span class="chip">UI-AN-001.populated</span><span class="chip">UI-AN-001.error</span><span class="chip">UI-AN-001.permission_denied</span><span class="chip">UI-AN-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-an-002</code></td><td><span class="chip">UI-AN-002.initial</span><span class="chip">UI-AN-002.loading</span><span class="chip">UI-AN-002.populated</span><span class="chip">UI-AN-002.error</span><span class="chip">UI-AN-002.permission_denied</span><span class="chip">UI-AN-002.recovery</span></td><td><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-an-003</code></td><td><span class="chip">UI-AN-003.initial</span><span class="chip">UI-AN-003.loading</span><span class="chip">UI-AN-003.populated</span><span class="chip">UI-AN-003.error</span><span class="chip">UI-AN-003.permission_denied</span><span class="chip">UI-AN-003.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-004</code></td><td><span class="chip">UI-AN-004.initial</span><span class="chip">UI-AN-004.loading</span><span class="chip">UI-AN-004.populated</span><span class="chip">UI-AN-004.error</span><span class="chip">UI-AN-004.permission_denied</span><span class="chip">UI-AN-004.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-005</code></td><td><span class="chip">UI-AN-005.initial</span><span class="chip">UI-AN-005.loading</span><span class="chip">UI-AN-005.populated</span><span class="chip">UI-AN-005.error</span><span class="chip">UI-AN-005.permission_denied</span><span class="chip">UI-AN-005.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-006</code></td><td><span class="chip">UI-AN-006.initial</span><span class="chip">UI-AN-006.loading</span><span class="chip">UI-AN-006.populated</span><span class="chip">UI-AN-006.error</span><span class="chip">UI-AN-006.permission_denied</span><span class="chip">UI-AN-006.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-007</code></td><td><span class="chip">UI-AN-007.initial</span><span class="chip">UI-AN-007.loading</span><span class="chip">UI-AN-007.populated</span><span class="chip">UI-AN-007.error</span><span class="chip">UI-AN-007.permission_denied</span><span class="chip">UI-AN-007.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-008</code></td><td><span class="chip">UI-AN-008.initial</span><span class="chip">UI-AN-008.loading</span><span class="chip">UI-AN-008.populated</span><span class="chip">UI-AN-008.error</span><span class="chip">UI-AN-008.permission_denied</span><span class="chip">UI-AN-008.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-009</code></td><td><span class="chip">UI-AN-009.initial</span><span class="chip">UI-AN-009.loading</span><span class="chip">UI-AN-009.populated</span><span class="chip">UI-AN-009.error</span><span class="chip">UI-AN-009.permission_denied</span><span class="chip">UI-AN-009.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-010</code></td><td><span class="chip">UI-AN-010.initial</span><span class="chip">UI-AN-010.loading</span><span class="chip">UI-AN-010.populated</span><span class="chip">UI-AN-010.error</span><span class="chip">UI-AN-010.permission_denied</span><span class="chip">UI-AN-010.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-011</code></td><td><span class="chip">UI-AN-011.initial</span><span class="chip">UI-AN-011.loading</span><span class="chip">UI-AN-011.populated</span><span class="chip">UI-AN-011.error</span><span class="chip">UI-AN-011.permission_denied</span><span class="chip">UI-AN-011.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-012</code></td><td><span class="chip">UI-AN-012.initial</span><span class="chip">UI-AN-012.loading</span><span class="chip">UI-AN-012.populated</span><span class="chip">UI-AN-012.error</span><span class="chip">UI-AN-012.permission_denied</span><span class="chip">UI-AN-012.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-an-013</code></td><td><span class="chip">UI-AN-013.initial</span><span class="chip">UI-AN-013.loading</span><span class="chip">UI-AN-013.populated</span><span class="chip">UI-AN-013.error</span><span class="chip">UI-AN-013.permission_denied</span><span class="chip">UI-AN-013.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-014</code></td><td><span class="chip">UI-AN-014.initial</span><span class="chip">UI-AN-014.loading</span><span class="chip">UI-AN-014.populated</span><span class="chip">UI-AN-014.error</span><span class="chip">UI-AN-014.permission_denied</span><span class="chip">UI-AN-014.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-an-015</code></td><td><span class="chip">UI-AN-015.initial</span><span class="chip">UI-AN-015.loading</span><span class="chip">UI-AN-015.populated</span><span class="chip">UI-AN-015.error</span><span class="chip">UI-AN-015.permission_denied</span><span class="chip">UI-AN-015.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-seg-001</code></td><td><span class="chip">UI-SEG-001.initial</span><span class="chip">UI-SEG-001.loading</span><span class="chip">UI-SEG-001.populated</span><span class="chip">UI-SEG-001.error</span><span class="chip">UI-SEG-001.permission_denied</span><span class="chip">UI-SEG-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-seg-002</code></td><td><span class="chip">UI-SEG-002.initial</span><span class="chip">UI-SEG-002.loading</span><span class="chip">UI-SEG-002.populated</span><span class="chip">UI-SEG-002.error</span><span class="chip">UI-SEG-002.permission_denied</span><span class="chip">UI-SEG-002.recovery</span></td><td><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-seg-003</code></td><td><span class="chip">UI-SEG-003.initial</span><span class="chip">UI-SEG-003.loading</span><span class="chip">UI-SEG-003.populated</span><span class="chip">UI-SEG-003.error</span><span class="chip">UI-SEG-003.permission_denied</span><span class="chip">UI-SEG-003.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-fcst-001</code></td><td><span class="chip">UI-FCST-001.initial</span><span class="chip">UI-FCST-001.loading</span><span class="chip">UI-FCST-001.populated</span><span class="chip">UI-FCST-001.error</span><span class="chip">UI-FCST-001.permission_denied</span><span class="chip">UI-FCST-001.recovery</span></td><td><span class="chip">ML</span><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-fcst-002</code></td><td><span class="chip">UI-FCST-002.initial</span><span class="chip">UI-FCST-002.loading</span><span class="chip">UI-FCST-002.populated</span><span class="chip">UI-FCST-002.error</span><span class="chip">UI-FCST-002.permission_denied</span><span class="chip">UI-FCST-002.recovery</span></td><td><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-fcst-003</code></td><td><span class="chip">UI-FCST-003.initial</span><span class="chip">UI-FCST-003.loading</span><span class="chip">UI-FCST-003.populated</span><span class="chip">UI-FCST-003.error</span><span class="chip">UI-FCST-003.permission_denied</span><span class="chip">UI-FCST-003.recovery</span></td><td><span class="chip">ML</span><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-fcst-004</code></td><td><span class="chip">UI-FCST-004.initial</span><span class="chip">UI-FCST-004.loading</span><span class="chip">UI-FCST-004.populated</span><span class="chip">UI-FCST-004.error</span><span class="chip">UI-FCST-004.permission_denied</span><span class="chip">UI-FCST-004.recovery</span></td><td><span class="chip">ML</span><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-fcst-005</code></td><td><span class="chip">UI-FCST-005.initial</span><span class="chip">UI-FCST-005.loading</span><span class="chip">UI-FCST-005.populated</span><span class="chip">UI-FCST-005.error</span><span class="chip">UI-FCST-005.permission_denied</span><span class="chip">UI-FCST-005.recovery</span></td><td><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-fcst-006</code></td><td><span class="chip">UI-FCST-006.initial</span><span class="chip">UI-FCST-006.loading</span><span class="chip">UI-FCST-006.populated</span><span class="chip">UI-FCST-006.error</span><span class="chip">UI-FCST-006.permission_denied</span><span class="chip">UI-FCST-006.recovery</span></td><td><span class="chip">ML</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-fcst-007</code></td><td><span class="chip">UI-FCST-007.initial</span><span class="chip">UI-FCST-007.loading</span><span class="chip">UI-FCST-007.populated</span><span class="chip">UI-FCST-007.error</span><span class="chip">UI-FCST-007.permission_denied</span><span class="chip">UI-FCST-007.recovery</span></td><td><span class="chip">ML</span><span class="chip">AN</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-promo-001</code></td><td><span class="chip">UI-PROMO-001.initial</span><span class="chip">UI-PROMO-001.loading</span><span class="chip">UI-PROMO-001.populated</span><span class="chip">UI-PROMO-001.error</span><span class="chip">UI-PROMO-001.permission_denied</span><span class="chip">UI-PROMO-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">WA</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-promo-002</code></td><td><span class="chip">UI-PROMO-002.initial</span><span class="chip">UI-PROMO-002.loading</span><span class="chip">UI-PROMO-002.populated</span><span class="chip">UI-PROMO-002.error</span><span class="chip">UI-PROMO-002.permission_denied</span><span class="chip">UI-PROMO-002.recovery</span></td><td><span class="chip">AN</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-promo-003</code></td><td><span class="chip">UI-PROMO-003.initial</span><span class="chip">UI-PROMO-003.loading</span><span class="chip">UI-PROMO-003.populated</span><span class="chip">UI-PROMO-003.error</span><span class="chip">UI-PROMO-003.permission_denied</span><span class="chip">UI-PROMO-003.recovery</span></td><td><span class="chip">AN</span><span class="chip">WA</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-dash-001</code></td><td><span class="chip">UI-DASH-001.initial</span><span class="chip">UI-DASH-001.loading</span><span class="chip">UI-DASH-001.populated</span><span class="chip">UI-DASH-001.error</span><span class="chip">UI-DASH-001.permission_denied</span><span class="chip">UI-DASH-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-dash-002</code></td><td><span class="chip">UI-DASH-002.initial</span><span class="chip">UI-DASH-002.loading</span><span class="chip">UI-DASH-002.populated</span><span class="chip">UI-DASH-002.error</span><span class="chip">UI-DASH-002.permission_denied</span><span class="chip">UI-DASH-002.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-dash-003</code></td><td><span class="chip">UI-DASH-003.initial</span><span class="chip">UI-DASH-003.loading</span><span class="chip">UI-DASH-003.populated</span><span class="chip">UI-DASH-003.error</span><span class="chip">UI-DASH-003.permission_denied</span><span class="chip">UI-DASH-003.recovery</span></td><td><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-rpt-001</code></td><td><span class="chip">UI-RPT-001.initial</span><span class="chip">UI-RPT-001.loading</span><span class="chip">UI-RPT-001.populated</span><span class="chip">UI-RPT-001.error</span><span class="chip">UI-RPT-001.permission_denied</span><span class="chip">UI-RPT-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-rpt-002</code></td><td><span class="chip">UI-RPT-002.initial</span><span class="chip">UI-RPT-002.loading</span><span class="chip">UI-RPT-002.populated</span><span class="chip">UI-RPT-002.error</span><span class="chip">UI-RPT-002.permission_denied</span><span class="chip">UI-RPT-002.recovery</span></td><td><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-rpt-003</code></td><td><span class="chip">UI-RPT-003.initial</span><span class="chip">UI-RPT-003.loading</span><span class="chip">UI-RPT-003.populated</span><span class="chip">UI-RPT-003.error</span><span class="chip">UI-RPT-003.permission_denied</span><span class="chip">UI-RPT-003.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-rpt-004</code></td><td><span class="chip">UI-RPT-004.initial</span><span class="chip">UI-RPT-004.loading</span><span class="chip">UI-RPT-004.populated</span><span class="chip">UI-RPT-004.error</span><span class="chip">UI-RPT-004.permission_denied</span><span class="chip">UI-RPT-004.recovery</span></td><td><span class="chip">AN</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-rpt-005</code></td><td><span class="chip">UI-RPT-005.initial</span><span class="chip">UI-RPT-005.loading</span><span class="chip">UI-RPT-005.populated</span><span class="chip">UI-RPT-005.error</span><span class="chip">UI-RPT-005.permission_denied</span><span class="chip">UI-RPT-005.recovery</span></td><td><span class="chip">AN</span><span class="chip">WA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-rpt-006</code></td><td><span class="chip">UI-RPT-006.initial</span><span class="chip">UI-RPT-006.loading</span><span class="chip">UI-RPT-006.populated</span><span class="chip">UI-RPT-006.error</span><span class="chip">UI-RPT-006.permission_denied</span><span class="chip">UI-RPT-006.recovery</span></td><td><span class="chip">AN</span><span class="chip">VW</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-rpt-007</code></td><td><span class="chip">UI-RPT-007.initial</span><span class="chip">UI-RPT-007.loading</span><span class="chip">UI-RPT-007.populated</span><span class="chip">UI-RPT-007.error</span><span class="chip">UI-RPT-007.permission_denied</span><span class="chip">UI-RPT-007.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-pipe-001</code></td><td><span class="chip">UI-PIPE-001.initial</span><span class="chip">UI-PIPE-001.loading</span><span class="chip">UI-PIPE-001.populated</span><span class="chip">UI-PIPE-001.error</span><span class="chip">UI-PIPE-001.permission_denied</span><span class="chip">UI-PIPE-001.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span><span class="chip">ML</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>48</td></tr><tr><td><code>coverage.ui-pipe-002</code></td><td><span class="chip">UI-PIPE-002.initial</span><span class="chip">UI-PIPE-002.loading</span><span class="chip">UI-PIPE-002.populated</span><span class="chip">UI-PIPE-002.error</span><span class="chip">UI-PIPE-002.permission_denied</span><span class="chip">UI-PIPE-002.recovery</span></td><td><span class="chip">AN</span><span class="chip">DS</span><span class="chip">ML</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-pipe-003</code></td><td><span class="chip">UI-PIPE-003.initial</span><span class="chip">UI-PIPE-003.loading</span><span class="chip">UI-PIPE-003.populated</span><span class="chip">UI-PIPE-003.error</span><span class="chip">UI-PIPE-003.permission_denied</span><span class="chip">UI-PIPE-003.recovery</span></td><td><span class="chip">owners</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-pipe-004</code></td><td><span class="chip">UI-PIPE-004.initial</span><span class="chip">UI-PIPE-004.loading</span><span class="chip">UI-PIPE-004.populated</span><span class="chip">UI-PIPE-004.error</span><span class="chip">UI-PIPE-004.permission_denied</span><span class="chip">UI-PIPE-004.recovery</span></td><td><span class="chip">AN</span><span class="chip">ML</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-ops-001</code></td><td><span class="chip">UI-OPS-001.initial</span><span class="chip">UI-OPS-001.loading</span><span class="chip">UI-OPS-001.populated</span><span class="chip">UI-OPS-001.error</span><span class="chip">UI-OPS-001.permission_denied</span><span class="chip">UI-OPS-001.recovery</span></td><td><span class="chip">OP</span><span class="chip">owners</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-ops-002</code></td><td><span class="chip">UI-OPS-002.initial</span><span class="chip">UI-OPS-002.loading</span><span class="chip">UI-OPS-002.populated</span><span class="chip">UI-OPS-002.error</span><span class="chip">UI-OPS-002.permission_denied</span><span class="chip">UI-OPS-002.recovery</span></td><td><span class="chip">OP</span><span class="chip">owners</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-ops-003</code></td><td><span class="chip">UI-OPS-003.initial</span><span class="chip">UI-OPS-003.loading</span><span class="chip">UI-OPS-003.populated</span><span class="chip">UI-OPS-003.error</span><span class="chip">UI-OPS-003.permission_denied</span><span class="chip">UI-OPS-003.recovery</span></td><td><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ops-004</code></td><td><span class="chip">UI-OPS-004.initial</span><span class="chip">UI-OPS-004.loading</span><span class="chip">UI-OPS-004.populated</span><span class="chip">UI-OPS-004.error</span><span class="chip">UI-OPS-004.permission_denied</span><span class="chip">UI-OPS-004.recovery</span></td><td><span class="chip">IA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-notify-001</code></td><td><span class="chip">UI-NOTIFY-001.initial</span><span class="chip">UI-NOTIFY-001.loading</span><span class="chip">UI-NOTIFY-001.populated</span><span class="chip">UI-NOTIFY-001.error</span><span class="chip">UI-NOTIFY-001.permission_denied</span><span class="chip">UI-NOTIFY-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-notify-002</code></td><td><span class="chip">UI-NOTIFY-002.initial</span><span class="chip">UI-NOTIFY-002.loading</span><span class="chip">UI-NOTIFY-002.populated</span><span class="chip">UI-NOTIFY-002.error</span><span class="chip">UI-NOTIFY-002.permission_denied</span><span class="chip">UI-NOTIFY-002.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-notify-003</code></td><td><span class="chip">UI-NOTIFY-003.initial</span><span class="chip">UI-NOTIFY-003.loading</span><span class="chip">UI-NOTIFY-003.populated</span><span class="chip">UI-NOTIFY-003.error</span><span class="chip">UI-NOTIFY-003.permission_denied</span><span class="chip">UI-NOTIFY-003.recovery</span></td><td><span class="chip">WA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-001</code></td><td><span class="chip">UI-ADMIN-001.initial</span><span class="chip">UI-ADMIN-001.loading</span><span class="chip">UI-ADMIN-001.populated</span><span class="chip">UI-ADMIN-001.error</span><span class="chip">UI-ADMIN-001.permission_denied</span><span class="chip">UI-ADMIN-001.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-002</code></td><td><span class="chip">UI-ADMIN-002.initial</span><span class="chip">UI-ADMIN-002.loading</span><span class="chip">UI-ADMIN-002.populated</span><span class="chip">UI-ADMIN-002.error</span><span class="chip">UI-ADMIN-002.permission_denied</span><span class="chip">UI-ADMIN-002.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-003</code></td><td><span class="chip">UI-ADMIN-003.initial</span><span class="chip">UI-ADMIN-003.loading</span><span class="chip">UI-ADMIN-003.populated</span><span class="chip">UI-ADMIN-003.error</span><span class="chip">UI-ADMIN-003.permission_denied</span><span class="chip">UI-ADMIN-003.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-004</code></td><td><span class="chip">UI-ADMIN-004.initial</span><span class="chip">UI-ADMIN-004.loading</span><span class="chip">UI-ADMIN-004.populated</span><span class="chip">UI-ADMIN-004.error</span><span class="chip">UI-ADMIN-004.permission_denied</span><span class="chip">UI-ADMIN-004.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-005</code></td><td><span class="chip">UI-ADMIN-005.initial</span><span class="chip">UI-ADMIN-005.loading</span><span class="chip">UI-ADMIN-005.populated</span><span class="chip">UI-ADMIN-005.error</span><span class="chip">UI-ADMIN-005.permission_denied</span><span class="chip">UI-ADMIN-005.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>36</td></tr><tr><td><code>coverage.ui-admin-006</code></td><td><span class="chip">UI-ADMIN-006.initial</span><span class="chip">UI-ADMIN-006.loading</span><span class="chip">UI-ADMIN-006.populated</span><span class="chip">UI-ADMIN-006.error</span><span class="chip">UI-ADMIN-006.permission_denied</span><span class="chip">UI-ADMIN-006.recovery</span></td><td><span class="chip">IA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-007</code></td><td><span class="chip">UI-ADMIN-007.initial</span><span class="chip">UI-ADMIN-007.loading</span><span class="chip">UI-ADMIN-007.populated</span><span class="chip">UI-ADMIN-007.error</span><span class="chip">UI-ADMIN-007.permission_denied</span><span class="chip">UI-ADMIN-007.recovery</span></td><td><span class="chip">IA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-008</code></td><td><span class="chip">UI-ADMIN-008.initial</span><span class="chip">UI-ADMIN-008.loading</span><span class="chip">UI-ADMIN-008.populated</span><span class="chip">UI-ADMIN-008.error</span><span class="chip">UI-ADMIN-008.permission_denied</span><span class="chip">UI-ADMIN-008.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-009</code></td><td><span class="chip">UI-ADMIN-009.initial</span><span class="chip">UI-ADMIN-009.loading</span><span class="chip">UI-ADMIN-009.populated</span><span class="chip">UI-ADMIN-009.error</span><span class="chip">UI-ADMIN-009.permission_denied</span><span class="chip">UI-ADMIN-009.recovery</span></td><td><span class="chip">IA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-010</code></td><td><span class="chip">UI-ADMIN-010.initial</span><span class="chip">UI-ADMIN-010.loading</span><span class="chip">UI-ADMIN-010.populated</span><span class="chip">UI-ADMIN-010.error</span><span class="chip">UI-ADMIN-010.permission_denied</span><span class="chip">UI-ADMIN-010.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-011</code></td><td><span class="chip">UI-ADMIN-011.initial</span><span class="chip">UI-ADMIN-011.loading</span><span class="chip">UI-ADMIN-011.populated</span><span class="chip">UI-ADMIN-011.error</span><span class="chip">UI-ADMIN-011.permission_denied</span><span class="chip">UI-ADMIN-011.recovery</span></td><td><span class="chip">IA</span><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-012</code></td><td><span class="chip">UI-ADMIN-012.initial</span><span class="chip">UI-ADMIN-012.loading</span><span class="chip">UI-ADMIN-012.populated</span><span class="chip">UI-ADMIN-012.error</span><span class="chip">UI-ADMIN-012.permission_denied</span><span class="chip">UI-ADMIN-012.recovery</span></td><td><span class="chip">IA</span><span class="chip">OP</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>24</td></tr><tr><td><code>coverage.ui-admin-013</code></td><td><span class="chip">UI-ADMIN-013.initial</span><span class="chip">UI-ADMIN-013.loading</span><span class="chip">UI-ADMIN-013.populated</span><span class="chip">UI-ADMIN-013.error</span><span class="chip">UI-ADMIN-013.permission_denied</span><span class="chip">UI-ADMIN-013.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-014</code></td><td><span class="chip">UI-ADMIN-014.initial</span><span class="chip">UI-ADMIN-014.loading</span><span class="chip">UI-ADMIN-014.populated</span><span class="chip">UI-ADMIN-014.error</span><span class="chip">UI-ADMIN-014.permission_denied</span><span class="chip">UI-ADMIN-014.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-015</code></td><td><span class="chip">UI-ADMIN-015.initial</span><span class="chip">UI-ADMIN-015.loading</span><span class="chip">UI-ADMIN-015.populated</span><span class="chip">UI-ADMIN-015.error</span><span class="chip">UI-ADMIN-015.permission_denied</span><span class="chip">UI-ADMIN-015.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-016</code></td><td><span class="chip">UI-ADMIN-016.initial</span><span class="chip">UI-ADMIN-016.loading</span><span class="chip">UI-ADMIN-016.populated</span><span class="chip">UI-ADMIN-016.error</span><span class="chip">UI-ADMIN-016.permission_denied</span><span class="chip">UI-ADMIN-016.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-017</code></td><td><span class="chip">UI-ADMIN-017.initial</span><span class="chip">UI-ADMIN-017.loading</span><span class="chip">UI-ADMIN-017.populated</span><span class="chip">UI-ADMIN-017.error</span><span class="chip">UI-ADMIN-017.permission_denied</span><span class="chip">UI-ADMIN-017.recovery</span></td><td><span class="chip">IA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-018</code></td><td><span class="chip">UI-ADMIN-018.initial</span><span class="chip">UI-ADMIN-018.loading</span><span class="chip">UI-ADMIN-018.populated</span><span class="chip">UI-ADMIN-018.error</span><span class="chip">UI-ADMIN-018.permission_denied</span><span class="chip">UI-ADMIN-018.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-org-001</code></td><td><span class="chip">UI-ORG-001.initial</span><span class="chip">UI-ORG-001.loading</span><span class="chip">UI-ORG-001.populated</span><span class="chip">UI-ORG-001.error</span><span class="chip">UI-ORG-001.permission_denied</span><span class="chip">UI-ORG-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-org-002</code></td><td><span class="chip">UI-ORG-002.initial</span><span class="chip">UI-ORG-002.loading</span><span class="chip">UI-ORG-002.populated</span><span class="chip">UI-ORG-002.error</span><span class="chip">UI-ORG-002.permission_denied</span><span class="chip">UI-ORG-002.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-people-001</code></td><td><span class="chip">UI-PEOPLE-001.initial</span><span class="chip">UI-PEOPLE-001.loading</span><span class="chip">UI-PEOPLE-001.populated</span><span class="chip">UI-PEOPLE-001.error</span><span class="chip">UI-PEOPLE-001.permission_denied</span><span class="chip">UI-PEOPLE-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-people-002</code></td><td><span class="chip">UI-PEOPLE-002.initial</span><span class="chip">UI-PEOPLE-002.loading</span><span class="chip">UI-PEOPLE-002.populated</span><span class="chip">UI-PEOPLE-002.error</span><span class="chip">UI-PEOPLE-002.permission_denied</span><span class="chip">UI-PEOPLE-002.recovery</span></td><td><span class="chip">allowed</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-019</code></td><td><span class="chip">UI-ADMIN-019.initial</span><span class="chip">UI-ADMIN-019.loading</span><span class="chip">UI-ADMIN-019.populated</span><span class="chip">UI-ADMIN-019.error</span><span class="chip">UI-ADMIN-019.permission_denied</span><span class="chip">UI-ADMIN-019.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-admin-020</code></td><td><span class="chip">UI-ADMIN-020.initial</span><span class="chip">UI-ADMIN-020.loading</span><span class="chip">UI-ADMIN-020.populated</span><span class="chip">UI-ADMIN-020.error</span><span class="chip">UI-ADMIN-020.permission_denied</span><span class="chip">UI-ADMIN-020.recovery</span></td><td><span class="chip">WA</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-help-001</code></td><td><span class="chip">UI-HELP-001.initial</span><span class="chip">UI-HELP-001.loading</span><span class="chip">UI-HELP-001.populated</span><span class="chip">UI-HELP-001.error</span><span class="chip">UI-HELP-001.permission_denied</span><span class="chip">UI-HELP-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-shell-auth</code></td><td><span class="chip">UI-SHELL-AUTH.initial</span><span class="chip">UI-SHELL-AUTH.loading</span><span class="chip">UI-SHELL-AUTH.populated</span><span class="chip">UI-SHELL-AUTH.error</span><span class="chip">UI-SHELL-AUTH.permission_denied</span><span class="chip">UI-SHELL-AUTH.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-shell-global</code></td><td><span class="chip">UI-SHELL-GLOBAL.initial</span><span class="chip">UI-SHELL-GLOBAL.loading</span><span class="chip">UI-SHELL-GLOBAL.populated</span><span class="chip">UI-SHELL-GLOBAL.error</span><span class="chip">UI-SHELL-GLOBAL.permission_denied</span><span class="chip">UI-SHELL-GLOBAL.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-shell-workspace</code></td><td><span class="chip">UI-SHELL-WORKSPACE.initial</span><span class="chip">UI-SHELL-WORKSPACE.loading</span><span class="chip">UI-SHELL-WORKSPACE.populated</span><span class="chip">UI-SHELL-WORKSPACE.error</span><span class="chip">UI-SHELL-WORKSPACE.permission_denied</span><span class="chip">UI-SHELL-WORKSPACE.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-shell-installation</code></td><td><span class="chip">UI-SHELL-INSTALLATION.initial</span><span class="chip">UI-SHELL-INSTALLATION.loading</span><span class="chip">UI-SHELL-INSTALLATION.populated</span><span class="chip">UI-SHELL-INSTALLATION.error</span><span class="chip">UI-SHELL-INSTALLATION.permission_denied</span><span class="chip">UI-SHELL-INSTALLATION.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-001</code></td><td><span class="chip">UI-OVR-001.initial</span><span class="chip">UI-OVR-001.loading</span><span class="chip">UI-OVR-001.populated</span><span class="chip">UI-OVR-001.error</span><span class="chip">UI-OVR-001.permission_denied</span><span class="chip">UI-OVR-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-002</code></td><td><span class="chip">UI-OVR-002.initial</span><span class="chip">UI-OVR-002.loading</span><span class="chip">UI-OVR-002.populated</span><span class="chip">UI-OVR-002.error</span><span class="chip">UI-OVR-002.permission_denied</span><span class="chip">UI-OVR-002.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-003</code></td><td><span class="chip">UI-OVR-003.initial</span><span class="chip">UI-OVR-003.loading</span><span class="chip">UI-OVR-003.populated</span><span class="chip">UI-OVR-003.error</span><span class="chip">UI-OVR-003.permission_denied</span><span class="chip">UI-OVR-003.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-004</code></td><td><span class="chip">UI-OVR-004.initial</span><span class="chip">UI-OVR-004.loading</span><span class="chip">UI-OVR-004.populated</span><span class="chip">UI-OVR-004.error</span><span class="chip">UI-OVR-004.permission_denied</span><span class="chip">UI-OVR-004.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-005</code></td><td><span class="chip">UI-OVR-005.initial</span><span class="chip">UI-OVR-005.loading</span><span class="chip">UI-OVR-005.populated</span><span class="chip">UI-OVR-005.error</span><span class="chip">UI-OVR-005.permission_denied</span><span class="chip">UI-OVR-005.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-006</code></td><td><span class="chip">UI-OVR-006.initial</span><span class="chip">UI-OVR-006.loading</span><span class="chip">UI-OVR-006.populated</span><span class="chip">UI-OVR-006.error</span><span class="chip">UI-OVR-006.permission_denied</span><span class="chip">UI-OVR-006.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-007</code></td><td><span class="chip">UI-OVR-007.initial</span><span class="chip">UI-OVR-007.loading</span><span class="chip">UI-OVR-007.populated</span><span class="chip">UI-OVR-007.error</span><span class="chip">UI-OVR-007.permission_denied</span><span class="chip">UI-OVR-007.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-008</code></td><td><span class="chip">UI-OVR-008.initial</span><span class="chip">UI-OVR-008.loading</span><span class="chip">UI-OVR-008.populated</span><span class="chip">UI-OVR-008.error</span><span class="chip">UI-OVR-008.permission_denied</span><span class="chip">UI-OVR-008.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-009</code></td><td><span class="chip">UI-OVR-009.initial</span><span class="chip">UI-OVR-009.loading</span><span class="chip">UI-OVR-009.populated</span><span class="chip">UI-OVR-009.error</span><span class="chip">UI-OVR-009.permission_denied</span><span class="chip">UI-OVR-009.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-010</code></td><td><span class="chip">UI-OVR-010.initial</span><span class="chip">UI-OVR-010.loading</span><span class="chip">UI-OVR-010.populated</span><span class="chip">UI-OVR-010.error</span><span class="chip">UI-OVR-010.permission_denied</span><span class="chip">UI-OVR-010.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-011</code></td><td><span class="chip">UI-OVR-011.initial</span><span class="chip">UI-OVR-011.loading</span><span class="chip">UI-OVR-011.populated</span><span class="chip">UI-OVR-011.error</span><span class="chip">UI-OVR-011.permission_denied</span><span class="chip">UI-OVR-011.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-012</code></td><td><span class="chip">UI-OVR-012.initial</span><span class="chip">UI-OVR-012.loading</span><span class="chip">UI-OVR-012.populated</span><span class="chip">UI-OVR-012.error</span><span class="chip">UI-OVR-012.permission_denied</span><span class="chip">UI-OVR-012.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-013</code></td><td><span class="chip">UI-OVR-013.initial</span><span class="chip">UI-OVR-013.loading</span><span class="chip">UI-OVR-013.populated</span><span class="chip">UI-OVR-013.error</span><span class="chip">UI-OVR-013.permission_denied</span><span class="chip">UI-OVR-013.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-014</code></td><td><span class="chip">UI-OVR-014.initial</span><span class="chip">UI-OVR-014.loading</span><span class="chip">UI-OVR-014.populated</span><span class="chip">UI-OVR-014.error</span><span class="chip">UI-OVR-014.permission_denied</span><span class="chip">UI-OVR-014.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-015</code></td><td><span class="chip">UI-OVR-015.initial</span><span class="chip">UI-OVR-015.loading</span><span class="chip">UI-OVR-015.populated</span><span class="chip">UI-OVR-015.error</span><span class="chip">UI-OVR-015.permission_denied</span><span class="chip">UI-OVR-015.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-016</code></td><td><span class="chip">UI-OVR-016.initial</span><span class="chip">UI-OVR-016.loading</span><span class="chip">UI-OVR-016.populated</span><span class="chip">UI-OVR-016.error</span><span class="chip">UI-OVR-016.permission_denied</span><span class="chip">UI-OVR-016.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-017</code></td><td><span class="chip">UI-OVR-017.initial</span><span class="chip">UI-OVR-017.loading</span><span class="chip">UI-OVR-017.populated</span><span class="chip">UI-OVR-017.error</span><span class="chip">UI-OVR-017.permission_denied</span><span class="chip">UI-OVR-017.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-018</code></td><td><span class="chip">UI-OVR-018.initial</span><span class="chip">UI-OVR-018.loading</span><span class="chip">UI-OVR-018.populated</span><span class="chip">UI-OVR-018.error</span><span class="chip">UI-OVR-018.permission_denied</span><span class="chip">UI-OVR-018.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-019</code></td><td><span class="chip">UI-OVR-019.initial</span><span class="chip">UI-OVR-019.loading</span><span class="chip">UI-OVR-019.populated</span><span class="chip">UI-OVR-019.error</span><span class="chip">UI-OVR-019.permission_denied</span><span class="chip">UI-OVR-019.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-020</code></td><td><span class="chip">UI-OVR-020.initial</span><span class="chip">UI-OVR-020.loading</span><span class="chip">UI-OVR-020.populated</span><span class="chip">UI-OVR-020.error</span><span class="chip">UI-OVR-020.permission_denied</span><span class="chip">UI-OVR-020.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-021</code></td><td><span class="chip">UI-OVR-021.initial</span><span class="chip">UI-OVR-021.loading</span><span class="chip">UI-OVR-021.populated</span><span class="chip">UI-OVR-021.error</span><span class="chip">UI-OVR-021.permission_denied</span><span class="chip">UI-OVR-021.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-022</code></td><td><span class="chip">UI-OVR-022.initial</span><span class="chip">UI-OVR-022.loading</span><span class="chip">UI-OVR-022.populated</span><span class="chip">UI-OVR-022.error</span><span class="chip">UI-OVR-022.permission_denied</span><span class="chip">UI-OVR-022.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-023</code></td><td><span class="chip">UI-OVR-023.initial</span><span class="chip">UI-OVR-023.loading</span><span class="chip">UI-OVR-023.populated</span><span class="chip">UI-OVR-023.error</span><span class="chip">UI-OVR-023.permission_denied</span><span class="chip">UI-OVR-023.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-024</code></td><td><span class="chip">UI-OVR-024.initial</span><span class="chip">UI-OVR-024.loading</span><span class="chip">UI-OVR-024.populated</span><span class="chip">UI-OVR-024.error</span><span class="chip">UI-OVR-024.permission_denied</span><span class="chip">UI-OVR-024.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-ovr-025</code></td><td><span class="chip">UI-OVR-025.initial</span><span class="chip">UI-OVR-025.loading</span><span class="chip">UI-OVR-025.populated</span><span class="chip">UI-OVR-025.error</span><span class="chip">UI-OVR-025.permission_denied</span><span class="chip">UI-OVR-025.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-sys-001</code></td><td><span class="chip">UI-SYS-001.initial</span><span class="chip">UI-SYS-001.loading</span><span class="chip">UI-SYS-001.populated</span><span class="chip">UI-SYS-001.error</span><span class="chip">UI-SYS-001.permission_denied</span><span class="chip">UI-SYS-001.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-sys-002</code></td><td><span class="chip">UI-SYS-002.initial</span><span class="chip">UI-SYS-002.loading</span><span class="chip">UI-SYS-002.populated</span><span class="chip">UI-SYS-002.error</span><span class="chip">UI-SYS-002.permission_denied</span><span class="chip">UI-SYS-002.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-sys-003</code></td><td><span class="chip">UI-SYS-003.initial</span><span class="chip">UI-SYS-003.loading</span><span class="chip">UI-SYS-003.populated</span><span class="chip">UI-SYS-003.error</span><span class="chip">UI-SYS-003.permission_denied</span><span class="chip">UI-SYS-003.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-sys-004</code></td><td><span class="chip">UI-SYS-004.initial</span><span class="chip">UI-SYS-004.loading</span><span class="chip">UI-SYS-004.populated</span><span class="chip">UI-SYS-004.error</span><span class="chip">UI-SYS-004.permission_denied</span><span class="chip">UI-SYS-004.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr><tr><td><code>coverage.ui-sys-005</code></td><td><span class="chip">UI-SYS-005.initial</span><span class="chip">UI-SYS-005.loading</span><span class="chip">UI-SYS-005.populated</span><span class="chip">UI-SYS-005.error</span><span class="chip">UI-SYS-005.permission_denied</span><span class="chip">UI-SYS-005.recovery</span></td><td><span class="chip">all</span></td><td><span class="chip">ru</span><span class="chip">en</span></td><td><span class="chip">graphite</span></td><td><span class="quiet">—</span></td><td>12</td></tr></tbody></table></div></section>
  <section><div class="section-head"><h2>Design waves</h2></div><div class="table-wrap"><table><thead><tr><th>Wave</th><th>Title</th><th>Families</th><th>Depends on</th><th>Gate</th></tr></thead><tbody><tr><td><code>wave.g5.01</code></td><td>G5 bounded wave 01</td><td><span class="chip">family.auth.shell-auth.baseline-exception-auth</span><span class="chip">family.auth.shell-workspace.baseline</span><span class="chip">family.core.shell-workspace.baseline</span><span class="chip">family.data.shell-workspace.baseline</span></td><td><span class="quiet">—</span></td><td>G5</td></tr><tr><td><code>wave.g5.02</code></td><td>G5 bounded wave 02</td><td><span class="chip">family.dq.shell-workspace.baseline</span><span class="chip">family.an.shell-workspace.baseline</span><span class="chip">family.seg.shell-workspace.baseline</span><span class="chip">family.fcst.shell-workspace.baseline</span><span class="chip">family.promo.shell-workspace.baseline</span><span class="chip">family.dash.shell-workspace.baseline</span></td><td><span class="chip">wave.g5.01</span></td><td>G5</td></tr><tr><td><code>wave.g5.03</code></td><td>G5 bounded wave 03</td><td><span class="chip">family.rpt.shell-workspace.baseline</span><span class="chip">family.pipe.shell-workspace.baseline</span><span class="chip">family.ops.shell-workspace.baseline</span><span class="chip">family.ops.shell-setup.baseline-exception-setup</span><span class="chip">family.notify.shell-workspace.baseline</span><span class="chip">family.admin.shell-setup.baseline-exception-setup</span><span class="chip">family.admin.shell-workspace.baseline</span><span class="chip">family.org.shell-workspace.baseline</span></td><td><span class="chip">wave.g5.02</span></td><td>G5</td></tr><tr><td><code>wave.g5.04</code></td><td>G5 bounded wave 04</td><td><span class="chip">family.people.shell-workspace.baseline</span><span class="chip">family.help.shell-workspace.baseline</span><span class="chip">family.shell.shell-auth.baseline-exception-auth</span><span class="chip">family.shell.shell-workspace.baseline</span><span class="chip">family.shell.shell-setup.baseline-exception-setup</span><span class="chip">family.ovr.shell-workspace.baseline</span><span class="chip">family.ovr.shell-focus.baseline-exception-focus</span><span class="chip">family.sys.shell-system.baseline-exception-system</span></td><td><span class="chip">wave.g5.03</span></td><td>G5</td></tr></tbody></table></div></section>
  <section><header class="section-head"><h2>family.admin.shell-setup.baseline-exception-setup</h2><span>14 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-001</code>
                    
                  </div>
                  <h3>UI-ADMIN-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the overview contract for /admin</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the overview contract for /admin</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-001.installation.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-002</code>
                    
                  </div>
                  <h3>UI-ADMIN-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/workspaces</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/workspaces</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-002.installation.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-005</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-ADMIN-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/capacity</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/capacity</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-ADMIN-005.installation.manage</span><span class="chip">UI-ADMIN-005.workspace.manage</span><span class="chip">journey.adoption-and-performance-operations.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-006</code>
                    
                  </div>
                  <h3>UI-ADMIN-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the operator contract for /admin/services</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the operator contract for /admin/services</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-ADMIN-006.inspect</span><span class="chip">journey.adoption-and-performance-operations.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-007</code>
                    
                  </div>
                  <h3>UI-ADMIN-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the operator contract for /admin/workers</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the operator contract for /admin/workers</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-007.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-008</code>
                    
                  </div>
                  <h3>UI-ADMIN-008</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-008</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/plugins</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/plugins</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-008.plugin.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-009</code>
                    
                  </div>
                  <h3>UI-ADMIN-009</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-009</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/storage-backup</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/storage-backup</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-009.installation.backup_restore</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-010</code>
                    
                  </div>
                  <h3>UI-ADMIN-010</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-010</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /audit</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /audit</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-010.audit.read</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-011</code>
                    
                  </div>
                  <h3>UI-ADMIN-011</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-011</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /admin/localization-themes</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /admin/localization-themes</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-ADMIN-011.installation.manage</span><span class="chip">UI-ADMIN-011.workspace.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-012</code>
                    
                  </div>
                  <h3>UI-ADMIN-012</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-012</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /admin/system</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /admin/system</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-012.installation.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-014</code>
                    
                  </div>
                  <h3>UI-ADMIN-014</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-014</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/brand-profiles</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/brand-profiles</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-014.brand.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-015</code>
                    
                  </div>
                  <h3>UI-ADMIN-015</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-015</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /admin/brand-profiles/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /admin/brand-profiles/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-015.brand.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-016</code>
                    
                  </div>
                  <h3>UI-ADMIN-016</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-016</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /admin/company-packs</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /admin/company-packs</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-016.company_pack.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-017</code>
                    
                  </div>
                  <h3>UI-ADMIN-017</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-017</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /admin/company-packs/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /admin/company-packs/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-017.company_pack.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.admin.shell-workspace.baseline</h2><span>6 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-003</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-ADMIN-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/access</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/access</span></div>
                  <div class="label">Actions (4)</div><div class="chips"><span class="chip">UI-ADMIN-003.workspace.members.manage</span><span class="chip">UI-ADMIN-003.workspace.roles.assign</span><span class="chip">UI-ADMIN-003.report_access.manage</span><span class="chip">UI-ADMIN-003.dashboard_access.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-004</code>
                    
                  </div>
                  <h3>UI-ADMIN-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/policies</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/policies</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-004.workspace.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-013</code>
                    
                  </div>
                  <h3>UI-ADMIN-013</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-013</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/branding</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/branding</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ADMIN-013.brand.assign</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-018</code>
                    
                  </div>
                  <h3>UI-ADMIN-018</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-018</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/access/:resourceType/:resourceId</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/access/:resourceType/:resourceId</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-ADMIN-018.report_access.manage</span><span class="chip">UI-ADMIN-018.dashboard_access.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-019</code>
                    
                  </div>
                  <h3>UI-ADMIN-019</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-019</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/organization</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/organization</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-ADMIN-019.organization.manage</span><span class="chip">UI-ADMIN-019.organization.members.assign</span><span class="chip">UI-ADMIN-019.organization.leadership.assign</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ADMIN-020</code>
                    
                  </div>
                  <h3>UI-ADMIN-020</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-admin-020</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/organization/:orgUnitKey</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/organization/:orgUnitKey</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-ADMIN-020.organization.data_policy.manage</span><span class="chip">UI-ADMIN-020.organization.access.delegate</span><span class="chip">UI-ADMIN-020.organization.ownership.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.an.shell-workspace.baseline</h2><span>15 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-001</code>
                    
                  </div>
                  <h3>UI-AN-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analyses</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analyses</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-001.analysis.run</span><span class="chip">UI-AN-001.analysis.manage</span><span class="chip">UI-AN-001.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-002</code>
                    
                  </div>
                  <h3>UI-AN-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/analyses/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/analyses/new</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-002.analysis.run</span><span class="chip">UI-AN-002.analysis.manage</span><span class="chip">UI-AN-002.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-003</code>
                    
                  </div>
                  <h3>UI-AN-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the overview contract for /w/:workspaceKey/analytics/sales</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the overview contract for /w/:workspaceKey/analytics/sales</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-003.analysis.run</span><span class="chip">UI-AN-003.analysis.manage</span><span class="chip">UI-AN-003.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-004</code>
                    
                  </div>
                  <h3>UI-AN-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/customers</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/customers</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-004.analysis.run</span><span class="chip">UI-AN-004.analysis.manage</span><span class="chip">UI-AN-004.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-005</code>
                    
                  </div>
                  <h3>UI-AN-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/rfm</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/rfm</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-005.analysis.run</span><span class="chip">UI-AN-005.analysis.manage</span><span class="chip">UI-AN-005.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-006</code>
                    
                  </div>
                  <h3>UI-AN-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/cohorts</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/cohorts</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-006.analysis.run</span><span class="chip">UI-AN-006.analysis.manage</span><span class="chip">UI-AN-006.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-007</code>
                    
                  </div>
                  <h3>UI-AN-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/lifecycle</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/lifecycle</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-007.analysis.run</span><span class="chip">UI-AN-007.analysis.manage</span><span class="chip">UI-AN-007.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-008</code>
                    
                  </div>
                  <h3>UI-AN-008</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-008</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/basket</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/basket</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-008.analysis.run</span><span class="chip">UI-AN-008.analysis.manage</span><span class="chip">UI-AN-008.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-009</code>
                    
                  </div>
                  <h3>UI-AN-009</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-009</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/stores-channels</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/stores-channels</span></div>
                  <div class="label">Actions (4)</div><div class="chips"><span class="chip">UI-AN-009.analysis.run</span><span class="chip">UI-AN-009.analysis.manage</span><span class="chip">UI-AN-009.export.create</span><span class="chip">journey.digital-to-offline-unit-economics.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-010</code>
                    
                  </div>
                  <h3>UI-AN-010</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-010</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/margin-discounts</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/margin-discounts</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-010.analysis.run</span><span class="chip">UI-AN-010.analysis.manage</span><span class="chip">UI-AN-010.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-011</code>
                    
                  </div>
                  <h3>UI-AN-011</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-011</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/analyses/custom</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/analyses/custom</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-011.analysis.run</span><span class="chip">UI-AN-011.analysis.manage</span><span class="chip">UI-AN-011.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-012</code>
                    
                  </div>
                  <h3>UI-AN-012</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-012</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/analyses/:id/results/:runId</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/analyses/:id/results/:runId</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AN-012.analysis.run</span><span class="chip">UI-AN-012.analysis.manage</span><span class="chip">UI-AN-012.export.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-013</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-AN-013</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-013</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/research</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/research</span></div>
                  <div class="label">Actions (6)</div><div class="chips"><span class="chip">UI-AN-013.research.manage</span><span class="chip">UI-AN-013.finding.manage</span><span class="chip">UI-AN-013.comment.read</span><span class="chip">UI-AN-013.comment.create</span><span class="chip">UI-AN-013.comment.resolve</span><span class="chip">journey.publish-review-collaborate.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-014</code>
                    
                  </div>
                  <h3>UI-AN-014</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-014</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the workspace contract for /w/:workspaceKey/research/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the workspace contract for /w/:workspaceKey/research/:id</span></div>
                  <div class="label">Actions (6)</div><div class="chips"><span class="chip">UI-AN-014.research.manage</span><span class="chip">UI-AN-014.finding.manage</span><span class="chip">UI-AN-014.comment.read</span><span class="chip">UI-AN-014.comment.create</span><span class="chip">UI-AN-014.comment.resolve</span><span class="chip">journey.publish-review-collaborate.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AN-015</code>
                    
                  </div>
                  <h3>UI-AN-015</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-an-015</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/analytics/products</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/analytics/products</span></div>
                  <div class="label">Actions (4)</div><div class="chips"><span class="chip">UI-AN-015.analysis.run</span><span class="chip">UI-AN-015.analysis.manage</span><span class="chip">UI-AN-015.export.create</span><span class="chip">journey.product-category-assortment-inventory.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.auth.shell-auth.baseline-exception-auth</h2><span>4 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-AUTH-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.auth</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Compact sign-in editor for /auth/sign-in</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Authenticate, choose session persistence and language, or open the distinct recovery route</span></div>
                  <div class="label">Actions (4)</div><div class="chips"><span class="chip">UI-AUTH-001.submit-credentials</span><span class="chip">UI-AUTH-001.open-recovery</span><span class="chip">UI-AUTH-001.toggle-remember</span><span class="chip">UI-AUTH-001.change-language</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-002</code>
                    
                  </div>
                  <h3>UI-AUTH-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_flow</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.auth</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the wizard contract for /bootstrap</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the wizard contract for /bootstrap</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-AUTH-002.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-003</code>
                    
                  </div>
                  <h3>UI-AUTH-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_flow</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.auth</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the wizard contract for /invites/:token</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the wizard contract for /invites/:token</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-AUTH-003.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-004</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-AUTH-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_flow</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.auth</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Password recovery/reset wizard for /auth/recovery using a host/admin-issued reset token</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Validate an issued reset token, set a compliant password, and return safely to sign in</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-AUTH-004.validate-reset-token</span><span class="chip">UI-AUTH-004.set-new-password</span><span class="chip">UI-AUTH-004.return-sign-in</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.auth.shell-workspace.baseline</h2><span>2 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-005</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-AUTH-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_flow</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the wizard contract for /onboarding</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the wizard contract for /onboarding</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-AUTH-005.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-AUTH-006</code>
                    
                  </div>
                  <h3>UI-AUTH-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-auth-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /profile/security</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /profile/security</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-AUTH-006.api_token.manage_own</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.core.shell-workspace.baseline</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CORE-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-CORE-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-core-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the overview contract for /w/:workspaceKey/overview</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the overview contract for /w/:workspaceKey/overview</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-CORE-001.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.dash.shell-workspace.baseline</h2><span>3 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DASH-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-DASH-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dash-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/dashboards</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/dashboards</span></div>
                  <div class="label">Actions (6)</div><div class="chips"><span class="chip">UI-DASH-001.dashboard.manage</span><span class="chip">UI-DASH-001.dashboard.publish</span><span class="chip">UI-DASH-001.dashboard_access.manage</span><span class="chip">UI-DASH-001.comment.read</span><span class="chip">UI-DASH-001.comment.create</span><span class="chip">journey.refresh-with-stable-anchors.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DASH-002</code>
                    
                  </div>
                  <h3>UI-DASH-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dash-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/dashboards/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/dashboards/:id</span></div>
                  <div class="label">Actions (5)</div><div class="chips"><span class="chip">UI-DASH-002.dashboard.manage</span><span class="chip">UI-DASH-002.dashboard.publish</span><span class="chip">UI-DASH-002.dashboard_access.manage</span><span class="chip">UI-DASH-002.comment.read</span><span class="chip">UI-DASH-002.comment.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DASH-003</code>
                    
                  </div>
                  <h3>UI-DASH-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dash-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/dashboards/:id/edit</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/dashboards/:id/edit</span></div>
                  <div class="label">Actions (5)</div><div class="chips"><span class="chip">UI-DASH-003.dashboard.manage</span><span class="chip">UI-DASH-003.dashboard.publish</span><span class="chip">UI-DASH-003.dashboard_access.manage</span><span class="chip">UI-DASH-003.comment.read</span><span class="chip">UI-DASH-003.comment.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.data.shell-workspace.baseline</h2><span>31 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-DATA-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/connections</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/connections</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-DATA-001.connection.manage</span><span class="chip">UI-DATA-001.connection.secret.rotate</span><span class="chip">journey.data-to-trusted-result.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-002</code>
                    
                  </div>
                  <h3>UI-DATA-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/connections/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/connections/new</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-002.connection.manage</span><span class="chip">UI-DATA-002.connection.secret.rotate</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-003</code>
                    
                  </div>
                  <h3>UI-DATA-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/connections/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/connections/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-003.connection.manage</span><span class="chip">UI-DATA-003.connection.secret.rotate</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-004</code>
                    
                  </div>
                  <h3>UI-DATA-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/catalog</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/catalog</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-004.dataset.manage</span><span class="chip">journey.product-category-assortment-inventory.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-005</code>
                    
                  </div>
                  <h3>UI-DATA-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/catalog/objects/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/catalog/objects/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-005.dataset.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-006</code>
                    
                  </div>
                  <h3>UI-DATA-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/catalog/objects/:id/preview</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/catalog/objects/:id/preview</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-006.dataset.manage</span><span class="chip">UI-DATA-006.pii.preview</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-007</code>
                    
                  </div>
                  <h3>UI-DATA-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/datasets</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/datasets</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-007.dataset.manage</span><span class="chip">UI-DATA-007.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-008</code>
                    
                  </div>
                  <h3>UI-DATA-008</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-008</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/datasets/:id/mapping</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/datasets/:id/mapping</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-008.dataset.manage</span><span class="chip">UI-DATA-008.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-009</code>
                    
                  </div>
                  <h3>UI-DATA-009</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-009</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/datasets/:id/relationships</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/datasets/:id/relationships</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-009.dataset.manage</span><span class="chip">UI-DATA-009.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-010</code>
                    
                  </div>
                  <h3>UI-DATA-010</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-010</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/datasets/:id/policies</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/datasets/:id/policies</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-010.dataset.manage</span><span class="chip">UI-DATA-010.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-011</code>
                    
                  </div>
                  <h3>UI-DATA-011</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-011</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/datasets/:id/capabilities</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/datasets/:id/capabilities</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-011.dataset.manage</span><span class="chip">UI-DATA-011.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-012</code>
                    
                  </div>
                  <h3>UI-DATA-012</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-012</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/datasets/:id/versions</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/datasets/:id/versions</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-012.dataset.manage</span><span class="chip">UI-DATA-012.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-013</code>
                    
                  </div>
                  <h3>UI-DATA-013</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-013</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/metrics</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/metrics</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-013.metric.manage</span><span class="chip">UI-DATA-013.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-014</code>
                    
                  </div>
                  <h3>UI-DATA-014</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-014</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/metrics/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/metrics/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-014.metric.manage</span><span class="chip">UI-DATA-014.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-015</code>
                    
                  </div>
                  <h3>UI-DATA-015</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-015</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/filter-fields</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/filter-fields</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-015.dataset.manage</span><span class="chip">UI-DATA-015.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-016</code>
                    
                  </div>
                  <h3>UI-DATA-016</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-016</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/data-guides</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/data-guides</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-016.data_guide.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-017</code>
                    
                  </div>
                  <h3>UI-DATA-017</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-017</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/data-guides/:id/edit</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/data-guides/:id/edit</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-017.data_guide.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-018</code>
                    
                  </div>
                  <h3>UI-DATA-018</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-018</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the reader contract for /w/:workspaceKey/data-guides/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the reader contract for /w/:workspaceKey/data-guides/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-018.data_guide.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-019</code>
                    
                  </div>
                  <h3>UI-DATA-019</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-019</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/artifacts</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/artifacts</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-019.artifact.download</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-020</code>
                    
                  </div>
                  <h3>UI-DATA-020</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-020</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the overview contract for /w/:workspaceKey/datasets/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the overview contract for /w/:workspaceKey/datasets/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-020.dataset.manage</span><span class="chip">UI-DATA-020.dataset.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-021</code>
                    
                  </div>
                  <h3>UI-DATA-021</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-021</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/methodologies</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/methodologies</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-021.methodology.manage</span><span class="chip">UI-DATA-021.methodology.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-022</code>
                    
                  </div>
                  <h3>UI-DATA-022</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-022</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/methodologies/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/methodologies/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-022.methodology.manage</span><span class="chip">UI-DATA-022.methodology.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-023</code>
                    
                  </div>
                  <h3>UI-DATA-023</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-023</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/file-import-templates</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/file-import-templates</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-023.file_import_template.manage</span><span class="chip">UI-DATA-023.file_import_template.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-024</code>
                    
                  </div>
                  <h3>UI-DATA-024</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-024</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/file-import-templates/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/file-import-templates/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-024.file_import_template.manage</span><span class="chip">UI-DATA-024.file_import_template.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-025</code>
                    
                  </div>
                  <h3>UI-DATA-025</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-025</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/imports</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/imports</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-025.file_import.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-026</code>
                    
                  </div>
                  <h3>UI-DATA-026</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_flow</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-026</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the wizard contract for /w/:workspaceKey/imports/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the wizard contract for /w/:workspaceKey/imports/new</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DATA-026.file_import.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-027</code>
                    
                  </div>
                  <h3>UI-DATA-027</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-027</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/imports/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/imports/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-027.file_import.create</span><span class="chip">UI-DATA-027.run.retry</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-028</code>
                    
                  </div>
                  <h3>UI-DATA-028</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-028</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/metric-groups</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/metric-groups</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-028.metric.manage</span><span class="chip">UI-DATA-028.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-029</code>
                    
                  </div>
                  <h3>UI-DATA-029</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-029</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/metric-groups/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/metric-groups/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-029.metric.manage</span><span class="chip">UI-DATA-029.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-030</code>
                    
                  </div>
                  <h3>UI-DATA-030</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-030</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/number-formats</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/number-formats</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-030.metric.manage</span><span class="chip">UI-DATA-030.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DATA-031</code>
                    
                  </div>
                  <h3>UI-DATA-031</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.01</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-data-031</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/number-formats/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/number-formats/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DATA-031.metric.manage</span><span class="chip">UI-DATA-031.metric.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.dq.shell-workspace.baseline</h2><span>5 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DQ-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-DQ-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dq-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the overview contract for /w/:workspaceKey/data-quality</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the overview contract for /w/:workspaceKey/data-quality</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DQ-001.quality.manage</span><span class="chip">journey.data-to-trusted-result.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DQ-002</code>
                    
                  </div>
                  <h3>UI-DQ-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dq-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/quality-rules</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/quality-rules</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DQ-002.quality.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DQ-003</code>
                    
                  </div>
                  <h3>UI-DQ-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dq-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/quality-rules/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/quality-rules/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DQ-003.quality.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DQ-004</code>
                    
                  </div>
                  <h3>UI-DQ-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dq-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/quality-reports/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/quality-reports/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-DQ-004.quality.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-DQ-005</code>
                    
                  </div>
                  <h3>UI-DQ-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-dq-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/quality-issues/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/quality-issues/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-DQ-005.quality.manage</span><span class="chip">UI-DQ-005.quality.waiver.approve</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.fcst.shell-workspace.baseline</h2><span>7 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-FCST-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/forecasts</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/forecasts</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-001.forecast.train</span><span class="chip">UI-FCST-001.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-002</code>
                    
                  </div>
                  <h3>UI-FCST-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/forecasts/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/forecasts/new</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-002.forecast.train</span><span class="chip">UI-FCST-002.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-003</code>
                    
                  </div>
                  <h3>UI-FCST-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/forecasts/:id/backtests</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/forecasts/:id/backtests</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-003.forecast.train</span><span class="chip">UI-FCST-003.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-004</code>
                    
                  </div>
                  <h3>UI-FCST-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/forecasts/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/forecasts/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-004.forecast.train</span><span class="chip">UI-FCST-004.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-005</code>
                    
                  </div>
                  <h3>UI-FCST-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/models/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/models/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-005.forecast.train</span><span class="chip">UI-FCST-005.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-006</code>
                    
                  </div>
                  <h3>UI-FCST-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/forecasts/:id/monitoring</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/forecasts/:id/monitoring</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-006.forecast.train</span><span class="chip">UI-FCST-006.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-FCST-007</code>
                    
                  </div>
                  <h3>UI-FCST-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-fcst-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/models</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/models</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-FCST-007.forecast.train</span><span class="chip">UI-FCST-007.forecast.promote</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.help.shell-workspace.baseline</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-HELP-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-HELP-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-help-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /help</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /help</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-HELP-001.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.notify.shell-workspace.baseline</h2><span>3 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-NOTIFY-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-NOTIFY-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-notify-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /notifications</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /notifications</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-NOTIFY-001.notification.read</span><span class="chip">UI-NOTIFY-001.notification.acknowledge</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-NOTIFY-002</code>
                    
                  </div>
                  <h3>UI-NOTIFY-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-notify-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /notifications/preferences</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /notifications/preferences</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-NOTIFY-002.notification.read</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-NOTIFY-003</code>
                    
                  </div>
                  <h3>UI-NOTIFY-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-notify-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/settings/notification-channels</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/settings/notification-channels</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-NOTIFY-003.workspace.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.ops.shell-setup.baseline-exception-setup</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OPS-004</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-OPS-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ops-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the operator contract for /admin/runtime</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the operator contract for /admin/runtime</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OPS-004.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.ops.shell-workspace.baseline</h2><span>3 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OPS-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-OPS-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ops-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the operator contract for /w/:workspaceKey/runs</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the operator contract for /w/:workspaceKey/runs</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-OPS-001.run.create</span><span class="chip">UI-OPS-001.run.cancel</span><span class="chip">UI-OPS-001.run.retry</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OPS-002</code>
                    
                  </div>
                  <h3>UI-OPS-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ops-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/runs/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/runs/:id</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-OPS-002.run.create</span><span class="chip">UI-OPS-002.run.cancel</span><span class="chip">UI-OPS-002.run.retry</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OPS-003</code>
                    
                  </div>
                  <h3>UI-OPS-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ops-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/runs/:id/nodes/:nodeId/attempts/:attemptId</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/runs/:id/nodes/:nodeId/attempts/:attemptId</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-OPS-003.run.create</span><span class="chip">UI-OPS-003.run.cancel</span><span class="chip">UI-OPS-003.run.retry</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.org.shell-workspace.baseline</h2><span>2 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ORG-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-ORG-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-org-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/organization</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/organization</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ORG-001.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-ORG-002</code>
                    
                  </div>
                  <h3>UI-ORG-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-org-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/organization/:orgUnitKey</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/organization/:orgUnitKey</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-ORG-002.organization.activity.read</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.ovr.shell-focus.baseline-exception-focus</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-020</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-OVR-020</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_backed_transient</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-020</dd></div>
                    <div><dt>Shell</dt><dd>shell.focus</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Full-screen Focus / Explore Surface</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Full-screen Focus / Explore Surface</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-020.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.ovr.shell-workspace.baseline</h2><span>24 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-OVR-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Workspace switcher</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Workspace switcher</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-001.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-002</code>
                    
                  </div>
                  <h3>UI-OVR-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Global command palette</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Global command palette</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-002.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-003</code>
                    
                  </div>
                  <h3>UI-OVR-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Searchable Filter Explorer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Searchable Filter Explorer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-003.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-004</code>
                    
                  </div>
                  <h3>UI-OVR-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Filter expression editor</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Filter expression editor</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-004.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-005</code>
                    
                  </div>
                  <h3>UI-OVR-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Previous-year comparison editor</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Previous-year comparison editor</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-005.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-006</code>
                    
                  </div>
                  <h3>UI-OVR-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Result Trust drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Result Trust drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-006.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-007</code>
                    
                  </div>
                  <h3>UI-OVR-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Chart data table</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Chart data table</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-007.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-008</code>
                    
                  </div>
                  <h3>UI-OVR-008</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-008</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Publish diff and impact modal</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Publish diff and impact modal</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-008.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-009</code>
                    
                  </div>
                  <h3>UI-OVR-009</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-009</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Clone/deprecate/archive modal</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Clone/deprecate/archive modal</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-009.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-010</code>
                    
                  </div>
                  <h3>UI-OVR-010</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-010</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Operation progress drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Operation progress drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-010.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-011</code>
                    
                  </div>
                  <h3>UI-OVR-011</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-011</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Cancel/retry/rerun confirmation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Cancel/retry/rerun confirmation</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-011.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-012</code>
                    
                  </div>
                  <h3>UI-OVR-012</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-012</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Export preflight modal</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Export preflight modal</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-012.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-013</code>
                    
                  </div>
                  <h3>UI-OVR-013</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-013</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Email send confirmation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Email send confirmation</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-013.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-014</code>
                    
                  </div>
                  <h3>UI-OVR-014</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-014</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Promotion item detail drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Promotion item detail drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-014.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-015</code>
                    
                  </div>
                  <h3>UI-OVR-015</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-015</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Pipeline node inspector</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Pipeline node inspector</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-015.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-016</code>
                    
                  </div>
                  <h3>UI-OVR-016</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-016</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Notification detail drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Notification detail drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-016.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-017</code>
                    
                  </div>
                  <h3>UI-OVR-017</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-017</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Theme switcher</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Theme switcher</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-017.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-018</code>
                    
                  </div>
                  <h3>UI-OVR-018</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-018</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Permission/forbidden explanation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Permission/forbidden explanation</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-018.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-019</code>
                    
                  </div>
                  <h3>UI-OVR-019</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-019</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Destructive action confirmation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Destructive action confirmation</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-019.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-021</code>
                    
                  </div>
                  <h3>UI-OVR-021</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-021</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Help and contextual-help menu</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Help and contextual-help menu</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-021.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-022</code>
                    
                  </div>
                  <h3>UI-OVR-022</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-022</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Keyboard shortcuts reference</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Keyboard shortcuts reference</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-022.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-023</code>
                    
                  </div>
                  <h3>UI-OVR-023</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-023</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Unsaved changes confirmation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Unsaved changes confirmation</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-023.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-024</code>
                    
                  </div>
                  <h3>UI-OVR-024</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-024</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Discussion and comments drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Discussion and comments drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-024.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-OVR-025</code>
                    
                  </div>
                  <h3>UI-OVR-025</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>overlay</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-ovr-025</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Data treatment and sensitivity drawer</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Data treatment and sensitivity drawer</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-OVR-025.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.people.shell-workspace.baseline</h2><span>2 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PEOPLE-001</code>
                    
                  </div>
                  <h3>UI-PEOPLE-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-people-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/people</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/people</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-PEOPLE-001.organization.activity.read</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PEOPLE-002</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-PEOPLE-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-people-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/people/:principalId</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/people/:principalId</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PEOPLE-002.organization.activity.read</span><span class="chip">UI-PEOPLE-002.report.read</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.pipe.shell-workspace.baseline</h2><span>4 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PIPE-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-PIPE-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-pipe-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/pipelines</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/pipelines</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PIPE-001.pipeline.manage</span><span class="chip">UI-PIPE-001.pipeline.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PIPE-002</code>
                    
                  </div>
                  <h3>UI-PIPE-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-pipe-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/pipelines/:id/edit</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/pipelines/:id/edit</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PIPE-002.pipeline.manage</span><span class="chip">UI-PIPE-002.pipeline.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PIPE-003</code>
                    
                  </div>
                  <h3>UI-PIPE-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-pipe-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/pipelines/:id/versions</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/pipelines/:id/versions</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PIPE-003.pipeline.manage</span><span class="chip">UI-PIPE-003.pipeline.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PIPE-004</code>
                    
                  </div>
                  <h3>UI-PIPE-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-pipe-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/schedules</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/schedules</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PIPE-004.pipeline.manage</span><span class="chip">UI-PIPE-004.pipeline.publish</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.promo.shell-workspace.baseline</h2><span>3 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PROMO-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-PROMO-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-promo-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/promotions</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/promotions</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-PROMO-001.promotion.manage</span><span class="chip">journey.digital-to-offline-unit-economics.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PROMO-002</code>
                    
                  </div>
                  <h3>UI-PROMO-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-promo-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/promotions/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/promotions/new</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-PROMO-002.promotion.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-PROMO-003</code>
                    
                  </div>
                  <h3>UI-PROMO-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-promo-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/promotions/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/promotions/:id</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-PROMO-003.promotion.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.rpt.shell-workspace.baseline</h2><span>7 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-RPT-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/reports</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/reports</span></div>
                  <div class="label">Actions (5)</div><div class="chips"><span class="chip">UI-RPT-001.report.manage</span><span class="chip">UI-RPT-001.comment.read</span><span class="chip">UI-RPT-001.comment.create</span><span class="chip">journey.compose-large-workbook.1</span><span class="chip">journey.open-100x30-document-without-duplicate-compute.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-002</code>
                    
                  </div>
                  <h3>UI-RPT-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/reports/:id/edit</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/reports/:id/edit</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-RPT-002.report.manage</span><span class="chip">journey.compose-large-workbook.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-003</code>
                    
                  </div>
                  <h3>UI-RPT-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/reports/:id/snapshots/:sid</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/reports/:id/snapshots/:sid</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-RPT-003.report.manage</span><span class="chip">UI-RPT-003.comment.read</span><span class="chip">UI-RPT-003.comment.create</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-004</code>
                    
                  </div>
                  <h3>UI-RPT-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/reports/:id/send</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/reports/:id/send</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-RPT-004.report.send</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-005</code>
                    
                  </div>
                  <h3>UI-RPT-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/report-deliveries</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/report-deliveries</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-RPT-005.report.send</span><span class="chip">UI-RPT-005.run.retry</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-006</code>
                    
                  </div>
                  <h3>UI-RPT-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-006</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/exports</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/exports</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-RPT-006.export.create</span><span class="chip">UI-RPT-006.report.export_xlsx</span><span class="chip">UI-RPT-006.artifact.download</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-RPT-007</code>
                    
                  </div>
                  <h3>UI-RPT-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.03</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-rpt-007</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the settings contract for /w/:workspaceKey/settings/report-email</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the settings contract for /w/:workspaceKey/settings/report-email</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-RPT-007.report_email_policy.manage</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.seg.shell-workspace.baseline</h2><span>3 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SEG-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-SEG-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-seg-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the list contract for /w/:workspaceKey/segments</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the list contract for /w/:workspaceKey/segments</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-SEG-001.segment.manage</span><span class="chip">UI-SEG-001.segment.export</span><span class="chip">journey.define-recalculate-reuse-segment.1</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SEG-002</code>
                    
                  </div>
                  <h3>UI-SEG-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-seg-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the editor contract for /w/:workspaceKey/segments/new</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the editor contract for /w/:workspaceKey/segments/new</span></div>
                  <div class="label">Actions (3)</div><div class="chips"><span class="chip">UI-SEG-002.segment.manage</span><span class="chip">UI-SEG-002.segment.export</span><span class="chip">journey.define-recalculate-reuse-segment.2</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SEG-003</code>
                    
                  </div>
                  <h3>UI-SEG-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>route_screen</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.02</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-seg-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Provide the detail contract for /w/:workspaceKey/segments/:id</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Provide the detail contract for /w/:workspaceKey/segments/:id</span></div>
                  <div class="label">Actions (2)</div><div class="chips"><span class="chip">UI-SEG-003.segment.manage</span><span class="chip">UI-SEG-003.segment.export</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.shell.shell-auth.baseline-exception-auth</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SHELL-AUTH</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-SHELL-AUTH</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>persistent_shell</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-shell-auth</dd></div>
                    <div><dt>Shell</dt><dd>shell.auth</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Authentication shell</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Authentication shell</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SHELL-AUTH.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.shell.shell-setup.baseline-exception-setup</h2><span>1 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SHELL-INSTALLATION</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-SHELL-INSTALLATION</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>persistent_shell</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-shell-installation</dd></div>
                    <div><dt>Shell</dt><dd>shell.setup</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Installation administration shell</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Installation administration shell</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SHELL-INSTALLATION.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.shell.shell-workspace.baseline</h2><span>2 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SHELL-GLOBAL</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-SHELL-GLOBAL</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>persistent_shell</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-shell-global</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Global-user shell</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Global-user shell</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SHELL-GLOBAL.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SHELL-WORKSPACE</code>
                    
                  </div>
                  <h3>UI-SHELL-WORKSPACE</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>persistent_shell</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-shell-workspace</dd></div>
                    <div><dt>Shell</dt><dd>shell.workspace</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Workspace application shell</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Workspace application shell</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SHELL-WORKSPACE.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>family.sys.shell-system.baseline-exception-system</h2><span>5 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SYS-001</code>
                    <span class="representative">representative</span>
                  </div>
                  <h3>UI-SYS-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>system_state_family</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-sys-001</dd></div>
                    <div><dt>Shell</dt><dd>shell.system</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>403 Forbidden</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">403 Forbidden</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SYS-001.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SYS-002</code>
                    
                  </div>
                  <h3>UI-SYS-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>system_state_family</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-sys-002</dd></div>
                    <div><dt>Shell</dt><dd>shell.system</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>404 Not Found</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">404 Not Found</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SYS-002.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SYS-003</code>
                    
                  </div>
                  <h3>UI-SYS-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>system_state_family</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-sys-003</dd></div>
                    <div><dt>Shell</dt><dd>shell.system</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Session expired</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Session expired</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SYS-003.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SYS-004</code>
                    
                  </div>
                  <h3>UI-SYS-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>system_state_family</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-sys-004</dd></div>
                    <div><dt>Shell</dt><dd>shell.system</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Maintenance</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Maintenance</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SYS-004.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-SYS-005</code>
                    
                  </div>
                  <h3>UI-SYS-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>system_state_family</dd></div>
                    <div><dt>Scope</dt><dd>in_scope</dd></div>
                    <div><dt>Wave</dt><dd>wave.g5.04</dd></div>
                    <div><dt>Coverage</dt><dd>coverage.ui-sys-005</dd></div>
                    <div><dt>Shell</dt><dd>shell.system</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Upgrade required</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Upgrade required</span></div>
                  <div class="label">Actions (1)</div><div class="chips"><span class="chip">UI-SYS-005.inspect</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section><section><header class="section-head"><h2>unresolved-family</h2><span>24 screens</span></header><div class="screen-grid">
                <article class="screen-card">
                  <div class="screen-head">
                    <code>HISTORICAL-CUSTOMETRY-UI-V1</code>
                    
                  </div>
                  <h3>HISTORICAL-CUSTOMETRY-UI-V1</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>historical_exclusion</dd></div>
                    <div><dt>Scope</dt><dd>excluded</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Custometry UI Design Program V1 is terminal historical evidence only</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Custometry UI Design Program V1 is terminal historical evidence only</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>HISTORICAL-PENPOT</code>
                    
                  </div>
                  <h3>HISTORICAL-PENPOT</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>historical_exclusion</dd></div>
                    <div><dt>Scope</dt><dd>excluded</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Penpot evidence is historical and cannot be active visual authority</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Penpot evidence is historical and cannot be active visual authority</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-001</code>
                    
                  </div>
                  <h3>UI-CAP-001</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Workspace routing, guards and return</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Workspace routing, guards and return</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-002</code>
                    
                  </div>
                  <h3>UI-CAP-002</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Searchable typed filters</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Searchable typed filters</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-003</code>
                    
                  </div>
                  <h3>UI-CAP-003</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Previous-year comparison</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Previous-year comparison</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-004</code>
                    
                  </div>
                  <h3>UI-CAP-004</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Metric groups and adaptive formats</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Metric groups and adaptive formats</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-005</code>
                    
                  </div>
                  <h3>UI-CAP-005</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>ChartSpec visualization</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">ChartSpec visualization</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-006</code>
                    
                  </div>
                  <h3>UI-CAP-006</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Chart ↔ Data table</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Chart ↔ Data table</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-007</code>
                    
                  </div>
                  <h3>UI-CAP-007</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Focus / Explore</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Focus / Explore</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-008</code>
                    
                  </div>
                  <h3>UI-CAP-008</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Result Trust</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Result Trust</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-009</code>
                    
                  </div>
                  <h3>UI-CAP-009</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Research composition and findings</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Research composition and findings</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-010</code>
                    
                  </div>
                  <h3>UI-CAP-010</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Object-scoped comments</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Object-scoped comments</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-011</code>
                    
                  </div>
                  <h3>UI-CAP-011</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Resource access policy</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Resource access policy</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-012</code>
                    
                  </div>
                  <h3>UI-CAP-012</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>ReportSnapshot and export preflight</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">ReportSnapshot and export preflight</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-013</code>
                    
                  </div>
                  <h3>UI-CAP-013</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Verified-user report email</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Verified-user report email</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-014</code>
                    
                  </div>
                  <h3>UI-CAP-014</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Progress, ETA and cancellation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Progress, ETA and cancellation</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-015</code>
                    
                  </div>
                  <h3>UI-CAP-015</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Effective brand resolution</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Effective brand resolution</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-016</code>
                    
                  </div>
                  <h3>UI-CAP-016</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Authorized PII-safe rendering</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Authorized PII-safe rendering</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-017</code>
                    
                  </div>
                  <h3>UI-CAP-017</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Localization, accessibility and reduced motion</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Localization, accessibility and reduced motion</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-018</code>
                    
                  </div>
                  <h3>UI-CAP-018</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Governed population and outlier treatment</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Governed population and outlier treatment</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-019</code>
                    
                  </div>
                  <h3>UI-CAP-019</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Bucket, stratified and KMeans segmentation</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Bucket, stratified and KMeans segmentation</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-020</code>
                    
                  </div>
                  <h3>UI-CAP-020</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Discount components, cap and PVM trust</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Discount components, cap and PVM trust</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-021</code>
                    
                  </div>
                  <h3>UI-CAP-021</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Organization-scoped effective access and ownership</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Organization-scoped effective access and ownership</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                
                <article class="screen-card">
                  <div class="screen-head">
                    <code>UI-CAP-022</code>
                    
                  </div>
                  <h3>UI-CAP-022</h3>
                  <dl>
                    <div><dt>Route</dt><dd>—</dd></div>
                    <div><dt>Class</dt><dd>internal_or_non_visual</dd></div>
                    <div><dt>Scope</dt><dd>internal</dd></div>
                    <div><dt>Wave</dt><dd>unresolved</dd></div>
                    <div><dt>Coverage</dt><dd>unresolved</dd></div>
                    <div><dt>Shell</dt><dd>—</dd></div>
                  </dl>
                  <div class="label">Purpose</div><p>Privacy-safe People &amp; Creators</p>
                  <div class="label">User outcomes</div><div class="chips"><span class="chip">Privacy-safe People &amp; Creators</span></div>
                  <div class="label">Actions (0)</div><div class="chips"><span class="quiet">no actions</span></div>
                  <div class="label">Journeys</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Required states</div><div class="chips"><span class="quiet">—</span></div>
                  <div class="label">Unresolved</div><div class="chips"><span class="quiet">—</span></div>
                </article>
                </div></section>
</main>
</body>
</html>
