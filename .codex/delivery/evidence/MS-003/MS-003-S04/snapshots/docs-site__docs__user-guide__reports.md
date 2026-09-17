---
doc_id: sales-report-workspace
title: Sign in and work with a sales report
doc_version: 1
product_spec_version: 0.11.0-draft
locale: en
visibility: public
ship: true
audiences: [user]
route: /docs/user-guide/reports/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, REPORT-015, I18N-001]
proof_boundary:
  label: bounded-sales-report-user-guide
  exclusions: [packaged-runtime-readiness, published-reports]
reviewed_at: "2026-09-15"
---
# Sign in and work with a sales report

Ask your workspace administrator for your workspace identifier, email and password.
Open **Sign in**, enter those details and choose a language. If sign-in fails,
check the workspace identifier as well as your email and password. Contact your
administrator if you need new access details.

From **Report library**, choose **Create sales report** or open a saved draft.
The supplied source contains completed receipts in EUR. Refunds, cancelled
receipts and other currencies are excluded. The source rules are locked.

1. Enter a report title, period and Store. Choose a previous-year comparison if needed.
2. Select **Apply** to calculate those choices. A changed period or Store does not alter the saved result.
3. Review the chart, **Table** and **Result trust**, then select **Save** to persist the calculated draft.
4. Use **Open exact draft preview** to reopen that saved result. The preview is a draft, not a published report.

**Result trust** explains incomplete item attribution. The prepared source has
14,995 eligible item relationships out of 15,000, with five quarantined items;
the eligible receipt totals are retained. Coverage applies to the selected period.

Use the expand button to view the chart and complete table together. **Escape**
or **Close Focus** returns focus to that button. You can switch languages without
changing the result.

If another tab saved a newer draft, your input stays visible. Copy any edits you
want to keep, then choose **Reload saved draft** and reapply them before saving.
If the session expires, sign in again; protected results are hidden. For an
unavailable saved result, use **Retry** when offered or contact your administrator.
For an empty period, choose another period and select **Apply**.

Publication, email, export and custom block authoring are not available in this
report workspace. Availability in an installed candidate depends on its version.

[Back to documentation](../index.md)
