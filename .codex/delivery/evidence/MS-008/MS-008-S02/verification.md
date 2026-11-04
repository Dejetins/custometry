# MS-008-S02 observed verification

Status: required local checks passed; independent source review findings closed.
The canonical journal owns stage acceptance. Whole C04 remains open.

## Backend and contract proof

- Real disposable PostgreSQL/API integration: 1 passed in 65.51s. Existing v1/v2
  snapshots, composer migration/replay/CAS/crash recovery, current authorization
  and revocation remain covered. New cases cover preflight/Apply identity,
  authoritative Store/grain scope, forbidden Store values, immutable locks,
  persisted-lock selected-block isolation, pair Save/get, rejected forged comparison
  payload (409 ARTIFACT_CORRUPT), and comparison without a selected pair.
- Presentation contract/unit and new Analytics scope suites: 140 passed in 0.82s.
  Pure lock-move and duplicate identity tests supplement the real API boundary.
- Strict Pyright on composer contracts/service/resolver and Analytics
  normalize/service/workspace contracts: 0 errors, 0 warnings.
- Ruff on changed scope/composer runtime and focused tests: pass.
- Web typecheck passed again after the final review repair.
- Web focused state/structure/route/presentation suites: 35 passed in 0.405s before
  the ordered-ancestry regression was added; final state/structure run: 16 passed
  in 0.311s, including that regression (unchanged route/presentation20 reused).
- Local grouped profile after final review repair: PASS, observed=true. Ruff and
  git diff --check also passed.

These checks used the activated repository toolchain and locked/no-sync Python
runtime. The disposable API runner used the already available PostgreSQL image
`sha256:5d004e058f520673f1f6edbad6b1603d5dab4c818e257c041889ef64672a8cc4`.
No dependency installation or retained-runtime operation was used.

## Browser boundary and repairs

The isolated real API/browser harness owns ports 58147/41747. Retained runtime
41746 and user report/workspace data were not edited. The English C04 scenario
passed in 52.4s (then 50.0s in the first full run), including inherited Store/month,
selected pair, block-local week override, stale pair invalidation, server
GRAIN_MISMATCH, Save/reload/exact preview and read-only effective context. It
observed exactly three Apply calls and two explicit Compare calls, with no extra
compute during scope editing, Save or preview. Screenshot was inspected.

Initial new-test issues were repaired: explicit select accessible labels; wait
for actual saved preview mount rather than a 10-second action wait; valid unique
scope binding identity; assertion of the actual 409 artifact-corruption contract;
correct pure helper placement and returned Store-list type. These initial failures
are not successful proof runs.

First whole browser run: six passed, two failed. C02 changeGrain did not wait for
new asynchronous validation before its next action; RU language switch did not
open the menu. Tests now await closed committed Builder and open the actual menu.
Final whole run: all 8 passed in 1.9 minutes, including C02 reconnect/unknown Save,
C03 hierarchy/history/RU+EN 200% document zoom and both C04 cases. RU proves direct
linked empty Store scope, keyboard Update scope, authoritative empty context and
Undo/Redo without additional Apply. EN proves delayed validation disables Save.
Final EN and RU screenshots were inspected. A final RU capture-only refinement
uses the scope element rather than the viewport; its unchanged behavior passed
again in 10.2s (17.5s including harness).

## Independent review repairs and closure

1. Selected source validation and persisted lock preservation previously resolved
   unrelated block inputs. Selected filtering now precedes effective resolution;
   lock preservation uses structural ancestry/direct links only. Reviewer closed
   this finding; real API covers persisted baseline A succeeds/B fails/full draft
   fails.
2. Scope validation could overlap Save. Scope and Builder now synchronously register
   unique in-flight validation tokens with the parent; Save guards the live token
   set and disables its button. Commits check a live saving/read-only ref. The
   browser delays a real validation response and checks Save remains disabled.
3. Client scope identity lost ancestry ordering. It now includes the ordered chain
   of applicable scope targets; a regression swaps nested context precedence and
   requires invalidation while unscoped structural movement retains reuse.

Full provider registry/evaluator, relationships/sequence/aggregate predicates,
resource budgets/estimates, windows/populations and unsupported comparison modes
remain unproved and open. This evidence is not production/release/performance or
full C10 accessibility/scale qualification.
