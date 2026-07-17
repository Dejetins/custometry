---
doc_id: docs-home
title: Документация Custometry
doc_version: 1
product_spec_version: 0.8.2-draft
locale: ru
visibility: public
ship: true
audiences: [installer, user]
route: /docs/ru/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004]
proof_boundary:
  label: foundation-public-documentation-home
  exclusions: [permission-aware-help-runtime, authenticated-document-serving]
reviewed_at: "2026-07-16"
---
# Документация Custometry

Custometry — локально разворачиваемая платформа клиентской аналитики и прогнозирования. Эта документация поставляется вместе с установленной версией и не зависит от внешнего сайта.

!!! info "Состояние Foundation"
    Текущий исполняемый контур проверяет Web-каркас, локальную документацию, health-границу API, миграцию control-plane PostgreSQL и детерминированный demo source. Продуктовая аналитика пока только запланирована.

- [Локальная установка](install/local.md)
- [Рабочее пространство Foundation](user-guide/foundation.md)

Публичная сборка документации не включает закрытые operator/admin runbooks, внутреннюю архитектуру, ADR, delivery tickets/evidence и журналы итераций.
