# Pilot comparison — first-run entry

Source: preserved `docs/architecture/ui/target-pilot/ru/source.html` at the accepted
manifest hash. Functional outcomes are recorded separately in [the report](report.md).
The source has no installer; the centered single-column entry is a derived layout.

| Rule | Source | Entry / assessment |
|---|---|---|
| Graphite hierarchy | canvas #070708, surface #111214, module #1a1b1e, border #303136 | Exact scoped tokens; no inherited blue Foundation surface |
| Type | 14px base, 17px compact h1, system/Inter fallback | Same stack and scale, no remote font; prose wraps |
| Panels/controls | 10px panels, 7px controls, 32px control height | Shared entry primitives use the same geometry; panels separate current status and next step |
| Actions/focus | cyan #8ccfe3 primary, #8bd2e8 two-pixel focus | Exact tokens and visible keyboard perimeter; native select and links |
| Icons/status | restrained outline icons, text and color | Lucide 17px/1.75 stroke, ready/failure/unknown text; no color-only meaning |
| Composition | compact product/report chrome and contextual content | Product identity/language chrome, 720px bounded status column; no rail before a workspace exists |
| Responsive | source inspected at all four ADR anchors | Same anchors; critical content and actions remain in document flow; zoom stacks/wraps as needed |

Matched screenshots are named `screenshots/web-{768,1024,1440,1920}-pilot-ru.png`
and `screenshots/web-{768,1024,1440,1920}-entry-ru.png`. English, zoom and pseudo
captures share the same viewport prefixes. The source captures retain the pilot's
fixture labels/data only as visual-reference evidence; none is rendered in the
installation entry. Failure captures show the actual API's loss of readiness.

Visual inspection found readable status and actions without clipped text in the
representative normal, failure, doubled-layout and long-text captures. Blank space
on larger anchors is deliberate: the installer has neither a report nor analytical
content to fill it. This is a bounded conformity assessment, not whole-pilot
implementation or the owner's S05 visual acceptance.

| Viewport | Source | Entry |
|---|---|---|
| 768x1024 | [Pilot](screenshots/web-768-pilot-ru.png) | [Russian entry](screenshots/web-768-entry-ru.png) |
| 1024x768 | [Pilot](screenshots/web-1024-pilot-ru.png) | [Russian entry](screenshots/web-1024-entry-ru.png) |
| 1440x900 | [Pilot](screenshots/web-1440-pilot-ru.png) | [Russian entry](screenshots/web-1440-entry-ru.png) |
| 1920x1080 | [Pilot](screenshots/web-1920-pilot-ru.png) | [Russian entry](screenshots/web-1920-entry-ru.png) |

[English](screenshots/web-1440-entry-en.png), [200% layout zoom](screenshots/web-768-zoom-ru.png), [long-text pseudo-locale](screenshots/web-768-pseudo.png), [API unavailable](screenshots/api-failure.png).
