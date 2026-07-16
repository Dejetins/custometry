---
doc_id: install-local
title: Локальная установка для разработки
doc_version: 2
product_spec_version: 0.8.2-draft
locale: ru
visibility: public
ship: true
audiences: [installer]
route: /docs/ru/install/local/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004]
proof_boundary:
  label: foundation-local-installation-guide
  exclusions: [release-artifact-acceptance, production-deployment-readiness]
reviewed_at: "2026-07-16"
---
# Локальная установка для разработки

Foundation пока не публикует принятый пользовательский release bundle. Поддерживаемый
сейчас путь предназначен для разработки из репозитория и собирает закреплённый checkout
через Docker Compose. Успешная публикация candidate images из защищённого `main` ещё не
делает их готовым пользовательским релизом.

```bash
./deploy/compose/bootstrap.sh --build
```

Команда выбирает свободный порт только на `127.0.0.1`, создаёт локальные secret-файлы,
собирает Web/API из текущего checkout, запускает PostgreSQL, выполняет отдельную
migration job и проверяет готовность Web/API.

Для тестовой retail-базы добавляется `--with-demo`. На хосте требуются `bash`, `curl`,
`openssl` и `python3`.

`--release` зарезервирован как fail-closed контракт будущего защищённого,
версионированного, checksummed и attested release bundle. Создавать `.release.env`
вручную нельзя. До появления полного принятого bundle пользовательская установка
релиза намеренно недоступна.
