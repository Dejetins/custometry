---
doc_id: foundation-workspace
title: Рабочее пространство Foundation
doc_version: 2
product_spec_version: 0.11.0-draft
locale: ru
visibility: public
ship: true
audiences: [user]
route: /docs/ru/user-guide/foundation/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004, UI-SHELL-001, UI-SHELL-002, UI-SHELL-003]
proof_boundary:
  label: foundation-workspace-user-guide
  exclusions: [product-analytics-readiness, authenticated-help-runtime]
reviewed_at: "2026-07-16"
---
# Рабочее пространство Foundation

Foundation намеренно остаётся небольшим. Он задаёт Frost shell, канонический реестр маршрутов, скрываемую навигацию с иконками, каталоги English/Russian, локальную Help-точку и видимый статус API.

Зарезервированные продуктовым blueprint маршруты показывают состояние **Запланированная поверхность**. Оно фиксирует контракт, но не изображает готовую продуктовую функцию.

Сейчас доступны:

- Foundation home на `/`;
- Help на `/help`;
- публичная локальная документация на `/docs/`;
- proxied liveness, readiness и version endpoints в `/api/`;
- клавиатурная навигация и reduced-motion режим.

Authentication, permission-aware Help, бизнес-данные, аналитика, задания, exports, email и административные действия добавляются только в принятых вертикальных срезах.
