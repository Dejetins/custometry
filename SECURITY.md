# Security Policy

## Reporting a vulnerability

Do not disclose an exploitable vulnerability in a public issue. Use GitHub private vulnerability reporting for `Dejetins/custometry` when available. If that channel is unavailable, contact the repository owner privately through the contact method shown on the GitHub organization/profile and include only the minimum information needed to reproduce the issue.

Do not include real credentials, customer data, raw PII, access tokens, cookies, private DSNs, or production payloads in a report.

## Supported state

The repository is currently a Foundation scaffold and does not claim a supported production release. Security fixes will target the latest maintained release once releases exist; exact support windows will be published with the first release policy.

## Repository security boundaries

- Web/API/data runtime egress is deny-by-default and may be enabled only for explicitly allowlisted connector, mail, or update paths.
- Edge is a secretless infrastructure ingress adapter separated from API by `edge_to_web`/`web_to_api`; Docker Compose does not portably prove Edge outbound denial, so production requires target-specific firewall/CNI-equivalent enforcement and runtime probes.
- PostgreSQL and internal services are not published to host interfaces by default.
- Secrets enter through local secret files/references and are excluded from Git and generated examples.
- Architecture internals, prompt packs, iteration evidence, and private operational details are not part of the normal installation documentation bundle.
