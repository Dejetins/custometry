# Corrected local demonstration

The original owner report remains available in the existing loopback demo:
http://127.0.0.1:41744/w/54384ac3-1445-4397-90e1-6ae1134ec965/reports/021f96f7-f92d-510a-85f3-718233b6babf/edit

Reload the browser to use the current Vite source. Session sign-in remains at
http://127.0.0.1:41744/auth/sign-in if the session has expired. The existing owner
session and report were not modified by the correction tests; tests create
separate synthetic reports in the task-owned fixture. No new server was started.

Inspect the report body: no company calendar settings, current/pinned version IDs
or calendar adoption. Date range and grain remain in Context. Financial labels
come from the stored company-calendar reference. Save/reopen retains exact values.
No settings page is claimed. The original API58144 / Web41744 processes remain
running for review, with their existing lifecycle and task-owned PostgreSQL.

Current fiscal chart/table/400px screenshots are in browser/. The synthetic fiscal
scenario uses calendar setup as a test precondition, never as a report interaction.
