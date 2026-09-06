---
doc_id: install-local
title: Локальная установка для разработки
doc_version: 3
product_spec_version: 0.11.0-draft
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

## Целевая машина и следующий установщик

Первая проверочная машина — Mac M5 Max с 36 GB RAM; отдельная Linux VM на ней используется для ограниченной проверки Linux. Это не подтверждение поддержки всех Linux-серверов. Существующие команды выше относятся к текущему Foundation. Следующий установщик предполагает заранее установленный контейнерный движок, готовые образы, автоматическую конфигурацию и миграции, затем bootstrap в браузере. Перенос экспериментальных данных в первую поставку не требуется; чужие хранилища сохраняются.
