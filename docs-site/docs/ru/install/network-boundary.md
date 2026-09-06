---
doc_id: network-boundary
title: Сетевая граница
doc_version: 3
product_spec_version: 0.11.0-draft
locale: ru
visibility: public
ship: true
audiences: [installer, operator]
route: /docs/ru/install/network-boundary/
status: active
owner: product-documentation
requirement_ids: [HELP-001, HELP-003, HELP-004, SEC-016, SEC-017, SEC-018]
proof_boundary:
  label: foundation-network-boundary-guide
  exclusions: [connector-egress-runtime, production-network-hardening]
reviewed_at: "2026-07-16"
---
# Сетевая граница

Прикладные сервисы Foundation не имеют общего исходящего маршрута в интернет. Web, API и PostgreSQL остаются во внутренних Docker-сетях. Отдельный secretless/read-only контейнер `edge` владеет loopback-привязкой host и пересылает запросы на фиксированный upstream `web:8080`.

Edge — инфраструктурный адаптер входа, а не продуктовый микросервис или bounded context. В нём нет бизнес-логики, credentials, writable state или выбираемого пользователем назначения. `edge_to_web` соединяет только Edge и Web, а отдельная `web_to_api` — только Web и API. Edge и API не имеют общей Docker-сети.

Docker Compose не предоставляет portable ingress-only network primitive. Для host port publication на поддерживаемых Docker Desktop targets Edge подключается к невнутренней transport bridge, которая может дать ему ambient outbound route. Fixed upstream ограничивает routing самого proxy, но не является firewall и не доказывает egress denial. Это не разрешение business egress: Web и API остаются internal и проходят negative Internet probes.

Строгий запрет исходящего трафика Edge — отдельный production-hardening этап. На каждой production target host firewall, CNI или эквивалентная policy должна разрешить только утверждённый host ingress и `Edge → Web`, запретить прямой доступ Edge к API, control/data services, Internet, private/link-local/metadata ranges и подтвердить правила positive/negative runtime probes.

| Граница | Значение по умолчанию |
|---|---|
| Edge → Web и proxied API | Свободный порт на `127.0.0.1`, выбранный bootstrap |
| Control PostgreSQL | Только внутренняя сеть |
| Demo source PostgreSQL | Только внутренняя сеть, профиль `demo` |
| Исходящий интернет Web/API | Отключён и проверяется negative probes |
| Edge → Web | Внутренняя `edge_to_web`; positive runtime probe |
| Web → API | Отдельная внутренняя `web_to_api`; Edge в неё не входит |
| Прямой Edge → API | Запрещён сегментацией и проверяется negative probe |
| Исходящий Edge transport | Может существовать в Foundation; строгий запрет требует target firewall/CNI evidence |

Браузер обращается к `/`, `/docs/` и `/api/*` через единственную Edge-точку; Web проксирует API route через `web_to_api`. Пароли создаются в игнорируемых secret-файлах и монтируются только в нужные сервисы; Edge не получает secrets.

## Принятый целевой HTTPS-режим

Текст выше описывает существующую HTTP Foundation-конфигурацию. Для следующей поставки принят HTTPS на Edge с единственным исключением: read-only TLS private key и certificate chain установки. Другие credentials и доменное состояние ему недоступны; выпуск и обновление сертификатов происходят вне Edge. Эта настройка ещё требует реализации и проверки. По умолчанию доступ остаётся локальным; явный LAN-режим должен пройти проверку из браузера другого компьютера. Production hardening сохраняет отдельную приёмку.
