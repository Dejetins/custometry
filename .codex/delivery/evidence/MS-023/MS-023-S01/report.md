# MS-023-S01 result

The public Semantic customer-events projection now binds genuine Customer, Receipt
and ReceiptItem artifacts, current-only mappings, exact native UTC receipt time and
publication cutoffs. Observed receipt rows are not inferred purchase/status-transition
events; history remains uncertified. No customer PII attributes are offered.

A separate nullable relationship admits null customer_id as unlinked while retaining
required namespace and nonnull-reference checks. The trusted root restriction limits
customers to those with at least one authorized observed receipt. SQL applies this
mandatory universe independently of the user expression and preserves receipt store
ceilings before root counting and event evaluation. No Python ID enumeration or raw
membership delivery. Unlinked rows do not become one artificial parent fanout, but
still consume row/byte input ceilings.

Explicit count-only customer-event catalog/preview endpoints and generated client
preserve old receipt roots/schemas. Catalog reauthenticates current read access;
preview also requires run access, resource action and cookie CSRF. Definition/time/
registry/universe/policy evidence is pinned and current grant changes prevent delivery.

Impact: compatible additive Semantic/Analytics/HTTP/client capability. No data or saved
report migration, calendar controls, browser mounting or production delivery. Genuine
provider and HTTP proof is distinct from the next saved cohort projection/editor unit.
Full Customer population, FILTER-015/C04 and C05–C11 remain outstanding.

[Verification](verification.md), [review](review.md), [manifest](manifest.json),
[canonical journal](../../../ledgers/MS-023.md).
