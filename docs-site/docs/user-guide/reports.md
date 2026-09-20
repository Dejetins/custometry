---
doc_id: sales-report-workspace
title: Sign in and work with a sales report
doc_version: 4
product_spec_version: 0.11.0-draft
locale: en
visibility: public
ship: true
audiences: [user]
route: /docs/user-guide/reports/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, REPORT-015, I18N-001, METRIC-025, METRIC-026, METRIC-027, METRIC-028, METRIC-030]
proof_boundary:
  label: bounded-sales-report-user-guide
  exclusions: [packaged-runtime-readiness, published-reports]
reviewed_at: "2026-09-21"
---
# Sign in and work with a sales report

Ask your workspace administrator for your workspace identifier, email and password.
Open **Sign in**, enter those details and choose a language. If sign-in fails,
check the workspace identifier as well as your email and password. Contact your
administrator if you need new access details.

From **Report library**, choose **Create sales report** or open a saved draft.
The supplied source contains completed receipts in EUR. Refunds, cancelled
receipts and other currencies are excluded. The source rules are locked.

For a saved report, use **Configure workset** to open the inspector. The creator
can add, copy and reorder personal worksets and cards. The catalog contains net
revenue, receipt count and average receipt. Repeated cards can use different
store restrictions. **Report context** controls the common dates, stores and
Day/Week/Month/Quarter/Half year/Year grain. An empty store selection means no data;
it does not mean all stores.

1. Change the required context or card settings, then choose **Apply**.
2. Review the chart, **Table**, exact dates and **Result Trust**.
3. Choose **Save report** to save all worksets and their results together.
4. Reopen the saved report or its **Exact snapshot**. Reopening does not calculate again.

Display-only edits can be saved using existing results. A reader works with the
accessible base and **My saved views**, using **Save personal view**. Personal
views do not change the author's worksets. Changing a query requires calculation
permission. A reader with an existing saved view can change its display and save
without running a new calculation.

Administrators open **Company settings · financial year** from administration
or the report. Choose the start month and whether the financial year is named
for its start or end year. Years start on the first day of the selected month;
the profile uses UTC and Monday weeks. April with end-year labels makes FY2026
run from 1 April 2025 through 31 March 2026.

Saving company settings leaves existing reports on their pinned calendar.
The creator chooses **Adopt company calendar**, **Apply**, then **Save report**
to use the new version. Readers cannot change this report setting.

**Focus** shows the chart and full table together. **Escape** closes Focus or
the inspector and returns focus to its opening control. Card and workset order
also have keyboard-accessible buttons. Language changes preserve result values.

A dash means no available value; zero remains zero. **Result Trust** explains
coverage and source limitations for the selected period. If another tab saved a
newer version, your input stays visible: preserve needed edits, choose
**Reload saved**, then reapply them. If the session expires, protected results
are hidden and you must sign in again.

New-report creation retains the original source/Apply/Save flow. Goals, shared
worksets, publication, email and export are unavailable here. Availability in an
installed candidate depends on its version.

[Back to documentation](../index.md)
